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
from typing import Callable, Dict, List

import pandas as pd
from lxml import etree


def unfold_node(
    node: etree._Element,
) -> tuple[str, dict[str, dict[str,]]]:
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
        data_nodes: list = node.xpath(f"./*")
        data: dict = {node.tag.partition("}")[2]: dict(map(unfold_node, data_nodes))}
        return {}, [data]
    if isinstance(subnode_tag, str):
        subnodes: list = node.findall(f"./{subnode_tag}", node.nsmap)
        metadata_nodes: list = node.xpath(
            f"./*[not(self::{subnode_tag})]", namespaces=node.nsmap
        )
        metadata: dict = {node.tag: dict(map(unfold_node, metadata_nodes))}
        return metadata, subnodes
    if isinstance(subnode_tag, list):
        # Handle multiple subnode types.
        raise NotImplementedError


class Tree_to_DataFrame:
    def __init__(self, subtree_to_dataframe: Callable, subtree_tag: str):
        self.subtree_to_dataframe = subtree_to_dataframe
        self.subtree_tag = subtree_tag

    def __call__(self, root):
        metadata, subtree_list = decompose_node(root, self.subtree_tag)
        meta_dict = pd.json_normalize(metadata).iloc[0].to_dict()
        subtree_dfs = [self.subtree_to_dataframe(subtree) for subtree in subtree_list]
        df = pd.concat(subtree_dfs, axis=0)
        df = df.assign(**meta_dict)
        return df


def Period_to_DataFrame_fn(get_Period_data: Callable) -> Callable:
    def Period_to_DataFrame(Period: etree._Element) -> pd.DataFrame:
        """
        Periods are implicitly valid as index is constructed independent from data extraction.
        Errors would occur at DataFrame construction.
        """
        index = get_Period_index(Period)
        data = get_Period_data(Period)
        assert len(data) == len(index)
        df = pd.DataFrame(data=data, index=index)

        metadata_nodes: list = Period.xpath(
            f"./*[not(self::Point)]", namespaces=Period.nsmap
        )
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
    "P1Y": "12M",
    "P1M": "1M",
    "P7D": "7D",
    "P1D": "1D",
    "PT60M": "60min",
    "PT30M": "30min",
    "PT15M": "15min",
    "PT1M": "1min",
}


def get_Period_data(Period: etree._Element) -> List[Dict]:
    points = Period.xpath("./Point", namespaces=Period.nsmap)
    data = [
        dict([(datum.tag, datum.text) for datum in point.iterchildren()])
        for point in points
    ]
    return data


def get_Period_Financial_Price_data(Period: etree._Element) -> List[Dict]:
    """
    TODO: Could be abstracted into `get_Period_data.
    """
    points = Period.xpath("./Point", namespaces=Period.nsmap)
    data = [get_Point_Financial_Price_data(point) for point in points]
    return data


def get_Point_Financial_Price_data(Point: etree._Element) -> Dict:
    """
    If a `Point` has overlapping `Financial_Price` field,
    the standard Procedure does not work.

    Applicable at e.g. FinancialExpensesAndIncomeForBalancing
    """
    direction_map = {"A01": "up", "A02": "down", "A03": "up_and_down"}

    datum = {Point.position.tag: Point.position.text}
    for fp in Point.Financial_Price:
        datum[
            ".".join([fp.tag, direction_map[fp.direction.text], fp.amount.tag])
        ] = fp.amount.text

    return datum


StandardPeriodParser = Period_to_DataFrame_fn(get_Period_data)
