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


def compose(*functions: List[Callable[[Any], Any]]) -> Callable[[Any], Any]:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def validate_timedeltas(filetype_parser: Callable[[requests.Response], pd.DataFrame]
                        ) -> Callable[[requests.Response], pd.DataFrame]:
    """
    TODO: Expand the logging to a validation functionality.
    """

    def parser_wrapper(response):
        df = filetype_parser(response)
        unique_timedeltas = df.index.to_series().diff().value_counts()
        log_msg = f"Unique pd.Timedelta counts:\n{unique_timedeltas}"
        if (unique_timedeltas.size > 1) and \
                ((unique_timedeltas.size == 2) and (unique_timedeltas.index.min() != pd.Timedelta(0))):
            logging.warning(log_msg)
            # raise IndexError
        else:
            logging.debug(log_msg)
        return df

    return parser_wrapper


@validate_timedeltas
def parse_zip(response: requests.Response) -> pd.DataFrame:
    archive = ZipFile(BytesIO(response.content), 'r')
    response_text_list = [archive.read(file).decode() for file in archive.infolist()]
    Period_to_DataFrame = Period_to_DataFrame_fn(get_Period_data)
    TimeSeries_to_DataFrame = TimeSeries_to_DataFrame_fn(Period_to_DataFrame)
    Response_to_DataFrame = Response_to_DataFrame_fn(TimeSeries_to_DataFrame)
    dataframe_list = [*map(Response_to_DataFrame, response_text_list)]
    df = pd.concat(dataframe_list, axis=0).sort_index()
    return df


@validate_timedeltas
def parse_text_xml(response: requests.Response) -> pd.DataFrame:
    response_text = response.text
    Period_to_DataFrame = Period_to_DataFrame_fn(get_Period_data)
    TimeSeries_to_DataFrame = TimeSeries_to_DataFrame_fn(Period_to_DataFrame)
    Response_to_DataFrame = Response_to_DataFrame_fn(TimeSeries_to_DataFrame)
    df = Response_to_DataFrame(response_text)
    return df


def parse_text_xml2(response: requests.Response) -> pd.DataFrame:
    response_text = response.text
    response_xml = drop_xml_encoding_line(response_text)
    root = etree.fromstring(response_xml)
    Point_to_DataFrame = Tree_to_DataFrame_fn(pd.json_normalize, None)
    Period_to_DataFrame = Tree_to_DataFrame_fn(Point_to_DataFrame, 'Point')
    TimeSeries_to_DataFrame = Tree_to_DataFrame_fn(Period_to_DataFrame, 'Period')
    Response_to_DataFrame = Tree_to_DataFrame_fn(TimeSeries_to_DataFrame, 'TimeSeries')
    df = Response_to_DataFrame(root)
    return df



def parse_outages(response: requests.Response) -> pd.DataFrame:
    """
    Outages responses do not contain `Periods` under the TimeSeries node.
    A `TimeSeries` node has to be unfolded and normalized to a single row.
    Further, they come as ZipFiles.
    """
    archive = ZipFile(BytesIO(response.content), 'r')
    response_text_list = [archive.read(file).decode() for file in archive.infolist()]
    TimeSeries_to_DataFrame = lambda TimeSeries: pd.json_normalize(dict([unfold_node(TimeSeries)]))
    Response_to_DataFrame = Response_to_DataFrame_fn(TimeSeries_to_DataFrame)
    dataframe_list = [*map(Response_to_DataFrame, response_text_list)]
    df = pd.concat(dataframe_list, axis=0).sort_index()
    return df


def parse_masterdata(response: requests.Response) -> pd.DataFrame:
    """
    MasterData responses do not contain `Periods` under the TimeSeries node.
    A `TimeSeries` node has to be unfolded and normalized to a single row.
    """
    response_text = response.text
    TimeSeries_to_DataFrame = lambda TimeSeries: pd.json_normalize(dict([unfold_node(TimeSeries)]))
    Response_to_DataFrame = Response_to_DataFrame_fn(TimeSeries_to_DataFrame)
    df = Response_to_DataFrame(response_text)
    return df


def parse_flowbasedparameters(response: requests.Response) -> pd.DataFrame:
    """
    Mostly custom functions for extraction below the `TimeSeries` level due to specific structure.
    TODO: Local functions do not pollute global nameSpace.
    """
    response_text = response.text

    def get_Constraint_TimeSeries_data(Constraint_TimeSeries: etree._Element) -> pd.DataFrame:
        ptdfs = Constraint_TimeSeries.findall('.//PTDF_Domain', Constraint_TimeSeries.nsmap)
        data = [dict((item.tag.partition('}')[2], item.text) for item in point) for point in ptdfs]
        df = pd.DataFrame(data)
        regres = Constraint_TimeSeries.findall('.//Monitored_RegisteredResource', Constraint_TimeSeries.nsmap)
        [res.remove(ptdf) for ptdf in ptdfs for res in regres]
        regres_data = [dict((item.tag.partition('}')[2], item.text) for item in point) for point in regres]
        regres_df = pd.DataFrame(regres_data)
        regres_df.columns = df.columns
        df = df.append(regres_df)
        df = pd.DataFrame(data=df['pTDF_Quantity.quantity'].values, index=df.mRID.values).T
        [Constraint_TimeSeries.remove(res) for res in regres]
        df = df.assign(**unfold_node(Constraint_TimeSeries)[1])
        return df

    def get_Point_data(Point: etree._Element) -> pd.DataFrame:
        constraint_timeseries = Point.findall('.//Constraint_TimeSeries', Point.nsmap)
        data = [get_Constraint_TimeSeries_data(cts) for cts in constraint_timeseries]
        df = pd.concat(data)
        [Point.remove(cts) for cts in constraint_timeseries]
        df = df.assign(**unfold_node(Point)[1])
        return df

    def get_Period_data(Period: etree._Element) -> List[pd.DataFrame]:
        points = Period.findall('.//Point', Period.nsmap)
        data = [get_Point_data(point) for point in points]
        return data

    def Period_to_DataFrame(Period: etree._Element) -> pd.DataFrame:
        """
        Specific to FlowbasedParameters.
        """
        index = get_Period_index(Period)
        df_list = get_Period_data(Period)
        df_list = [subdf.eval("index=@ix").set_index('index') for subdf, ix in zip(df_list, index)]
        df = pd.concat(df_list, axis=0)
        return df

    TimeSeries_to_DataFrame = TimeSeries_to_DataFrame_fn(Period_to_DataFrame)
    Response_to_DataFrame = Response_to_DataFrame_fn(TimeSeries_to_DataFrame)
    df = Response_to_DataFrame(response_text)
    return df


def drop_xml_encoding_line(xml_text: str) -> str:
    return "\n".join(xml_text.split('\n')[1:])


def unfold_node(node: etree._Element) -> tuple[str, dict[str, dict[str,]]]:
    """
    Recursive unfolding of a node into a dict.
    TODO: Ensure no overwriting of same dict-names in the unfolding.
    """
    tag: str = node.tag
    children: etree._Element = node.getchildren()
    if children == []:
        return (tag, node.text)
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

def standard_parsing(root: etree._Element):
    metadata_0, subnodes_0 = decompose_node(root, 'TimeSeries')
    metadata_1, subnodes_1 = decompose_node(subnodes_0[0], 'Period')
    metadata_2, subnodes_2 = decompose_node(subnodes_1[0], 'Point')
    data = decompose_node(subnodes_2[0], None)
    pd.json_normalize(data)


def traverse_tree(root: etree._Element, subnodes_tags: List[str]) -> List[Tuple[List[etree._Element],Dict[str, str]]]:
    """
    Recurvisely apply `decompose_node` with different tags for subnodes.
    Returns [metadata,
                [[metadata, [subnodes]],
                 [metadata, [subnodes]],
                  ...
                ]
             ]
    """
    if len(subnodes_tags) == 1:
        metadata, subnodes = decompose_node(root, subnodes_tags[0])
        return metadata, subnodes
    else:
        metadata, subnodes = decompose_node(root, subnodes_tags[0])
        return metadata, [traverse_tree(node, subnodes_tags[1:]) for node in subnodes]

def Tree_to_DataFrame_fn(Subtree_to_DataFrame: Callable, Subtree_Tag: str) -> Callable[[str], pd.DataFrame]:
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


parse_standard_format_response = compose(Response_to_DataFrame_fn,
                                          TimeSeries_to_DataFrame_fn,
                                          Period_to_DataFrame_fn,
                                          get_Period_data)

parse_standard_format_response = compose(
    get_Period_data,
    Period_to_DataFrame_fn,
    TimeSeries_to_DataFrame_fn,
    Response_to_DataFrame_fn
)