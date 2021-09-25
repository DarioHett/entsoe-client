"""
The XML Response format is a tree, where each node consists of meta-data and sub-nodes.
Typically, the tree decomposes as `root` -> `TimeSeries` -> `Period` -> `Point`.
A `point` is the smallest unit and holds `quantity` and `position` information.
A `period` holds meta-data on the `timeInterval` and `resolution` (=frequency) for
the contained `Points` it contains.
A `TimeSeries` is a collection of `Periods` with further metadata on the nature of a specific sub-domain of the query,
such as varying `Business Type` across TimeSeries'.
The root node holds meta-data on the global parameters of the query.

A minimal, trivial parser would purely unroll such structure recursively.
"""
# TODO: Testing suite.
import functools
import logging
from io import BytesIO
from typing import Callable, Dict, List, Any, Tuple
from zipfile import ZipFile

import pandas as pd
import requests
from lxml import etree


def unfold_node(node: etree._Element) -> tuple[str, dict[str, dict[str,]]]:
    """
    Recursive unfolding of a node into a dict.
    TODO: Ensure no overwriting of same dict-names in the unfolding.
    """
    tag: str = node.tag
    children: etree._Element = node.getchildren()
    if not children:
        return tag, node.text
    else:
        return tag, dict([unfold_node(child) for child in children])


def decompose_node(node: etree._Element, subnode_tag) -> tuple[dict, list]:
    """node -> [subnodes], {metadata}"""
    if not subnode_tag:
        data_nodes: list = node.xpath(f'./*')
        data: dict = {node.tag.partition('}')[2]: dict(map(unfold_node, data_nodes))}
        return {}, [data]
    if isinstance(subnode_tag, str):
        subnodes: list = node.findall(f"./{subnode_tag}", node.nsmap)
        metadata_nodes: list = node.xpath(f'./*[not(self::{subnode_tag})]',
                                      namespaces=node.nsmap)
        metadata: dict = {node.tag: dict(map(unfold_node, metadata_nodes))}
        return metadata, subnodes
    if isinstance(subnode_tag, list):
        # Handle multiple subnode types.
        raise NotImplementedError


def Tree_to_DataFrame_fn(Subtree_to_DataFrame: Callable, Subtree_Tag: str) -> Callable[[etree._Element], pd.DataFrame]:
    def Tree_to_DataFrame(root: etree._Element) -> pd.DataFrame:
        """
        """
        metadata, subtree_list = decompose_node(root, Subtree_Tag)
        meta_dict = pd.json_normalize(metadata).iloc[0].to_dict()
        subtree_dfs = [Subtree_to_DataFrame(subtree) for subtree in  subtree_list]
        df = pd.concat(subtree_dfs, axis=0)
        df = df.assign(**meta_dict)

        return df

    return Tree_to_DataFrame


class Tree_to_DataFrame:
    def __init__(self, subtree_to_dataframe: Callable, subtree_tag: str):
        self.subtree_to_dataframe = subtree_to_dataframe
        self.subtree_tag = subtree_tag

    def __call__(self, root):
        metadata, subtree_list = decompose_node(root, self.subtree_tag)
        meta_dict = pd.json_normalize(metadata).iloc[0].to_dict()
        subtree_dfs = [self.subtree_to_dataframe(subtree) for subtree in  subtree_list]
        df = pd.concat(subtree_dfs, axis=0)
        df = df.assign(**meta_dict)
        return df


def Response_to_DataFrame_fn(TimeSeries_to_DataFrame: Callable) -> Callable[[str], pd.DataFrame]:
    def Response_to_DataFrame(response_text: str) -> pd.DataFrame:
        """
        """
        response_xml = drop_xml_encoding_line(response_text)
        root = etree.fromstring(response_xml)

        # get_response_timeinterval = lambda string: root.find(f'./period.timeInterval/{string}', root.nsmap).text
        # logging.info(f"Start: {get_response_timeinterval('start')}, End: {get_response_timeinterval('end')}")
        metadata, TimeSeries_list = decompose_node(root, 'TimeSeries')
        meta_dict = pd.json_normalize(metadata, max_level=1).iloc[0].to_dict()
        TimeSeries_dfs = [TimeSeries_to_DataFrame(timeseries) for timeseries in TimeSeries_list]
        df = pd.concat(TimeSeries_dfs, axis=0)
        df = df.assign(**meta_dict)

        return df

    return Response_to_DataFrame


def TimeSeries_to_DataFrame_fn(Period_to_DataFrame: Callable) -> Callable:
    def TimeSeries_to_DataFrame(TimeSeries: etree._Element) -> pd.DataFrame:
        # BIG TODO: 4.2.4. Flow-based Parameters [11.1.B] seems particularly convoluted.
        metadata, periods = decompose_node(TimeSeries, 'Period')
        meta_dict = pd.json_normalize(metadata, max_level=1).iloc[0].to_dict()
        period_dfs = [Period_to_DataFrame(period) for period in periods]
        df = pd.concat(period_dfs, axis=0)
        df = df.assign(**meta_dict)
        return df

    return TimeSeries_to_DataFrame


def Period_to_DataFrame_fn(get_Period_data: Callable) -> Callable:
    def Period_to_DataFrame(Period: etree._Element) -> pd.DataFrame:
        """
        Periods are implcitly valid as index is constructed independent from data extraction.
        Errors would occur at DataFrame construction.
        """
        index = get_Period_index(Period)
        data = get_Period_data(Period)
        assert len(data) == len(index)
        df = pd.DataFrame(data=data, index=index)


        metadata_nodes: list = Period.xpath(f'./*[not(self::Point)]',
                                          namespaces=Period.nsmap)
        metadata: dict = {Period.tag: dict(map(unfold_node, metadata_nodes))}
        meta_dict = pd.json_normalize(metadata).iloc[0].to_dict()
        df = df.assign(**meta_dict)

        return df

    return Period_to_DataFrame


def get_Period_index(Period: etree._Element) -> pd.Index:
    start = Period.timeInterval.start.text
    end = Period.timeInterval.end.text
    resolution = Period.resolution.text
    index = pd.date_range(start, end, freq=resolution_map[resolution])
    index = index[:-1] if index.size > 1 else index
    return index


# Maps response_xml resolutions to
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html#pandas.Timedelta
resolution_map: Dict = {
    'P1Y': '12M',
    'P1M': '1M',
    'P7D': '7D',
    'P1D': '1D',
    'PT60M': '60min',
    'PT30M': '30min',
    'PT15M': '15min',
    'PT1M': '1min'
}


def get_Period_data(Period: etree._Element) -> List[Dict]:
    points = Period.xpath('./Point', namespaces=Period.nsmap)
    data = [dict([(datum.tag, datum.text) for datum in point.iterchildren()]) for point in points]
    return data


def get_Period_Financial_Price_data(Period: etree._Element) -> List[Dict]:
    """
    TODO: Could be abstracted into `get_Period_data.
    """
    points = Period.xpath('./Point', namespaces=Period.nsmap)
    data = [get_Point_Financial_Price_data(point) for point in points]
    return data


def get_Point_Financial_Price_data(Point: etree._Element) -> Dict:
    """
    If a `Point` has overlapping `Financial_Price` field,
    the standard Procedure does not work.

    Applicable at e.g. FinancialExpensesAndIncomeForBalancing
    """
    direction_map = {"A01": "up",
                     "A02": "down",
                     "A03": "up_and_down"}

    datum = {Point.position.tag: Point.position.text}
    for fp in Point.Financial_Price:
        datum['.'.join([fp.tag, direction_map[fp.direction.text], fp.amount.tag])] = fp.amount.text

    return datum


StandardPeriodParser = Period_to_DataFrame_fn(get_Period_data)
