# TODO: Testing suite.
import logging
from io import BytesIO
from typing import Callable, Dict, List
from zipfile import ZipFile, ZipInfo

import pandas as pd
import requests
from lxml import etree


def validate_timedeltas(filetype_parser: Callable[[requests.Response], pd.DataFrame]
                        ) -> Callable[[requests.Response], pd.DataFrame]:
    """
    TODO: Expand the logging to a validation functionality.
    """

    def filetype_parser_wrapper(response):
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

    return filetype_parser_wrapper


@validate_timedeltas
def parse_zip(response: requests.Response) -> pd.DataFrame:
    archive = ZipFile(BytesIO(response.content), 'r')
    files = archive.infolist()
    logging.debug(f"Files in response: {files}")
    File_to_DataFrame = ZipFile_to_DataFrame_func(archive)
    dataframe_list = map(File_to_DataFrame, files)
    df = pd.concat(dataframe_list, axis=0).sort_index()
    return df


def ZipFile_to_DataFrame_func(archive: ZipFile) -> Callable[[ZipInfo], pd.DataFrame]:
    def _file_to_dataframe(file: ZipInfo):
        response_text = archive.read(file).decode()
        Response_to_DataFrame = common_Response_to_DataFrame()
        return Response_to_DataFrame(response_text)

    return _file_to_dataframe


@validate_timedeltas
def parse_text_xml(response: requests.Response) -> pd.DataFrame:
    response_text = response.text
    Response_to_DataFrame = common_Response_to_DataFrame()
    df = Response_to_DataFrame(response_text)
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
    TODO: Local function do not pollute global nameSpace.
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

def common_Response_to_DataFrame() -> Callable[[str], pd.DataFrame]:
    """
    Avoids boilerplate code for `typical` parsers, e.g. such returning timeseries shaped data,
    where there is some metadata in each `TimeSeries` node with many `Points` under `Period`.
    """
    Period_to_DataFrame = Period_to_DataFrame_fn(get_Period_data)
    TimeSeries_to_DataFrame = TimeSeries_to_DataFrame_fn(Period_to_DataFrame)
    Response_to_DataFrame = Response_to_DataFrame_fn(TimeSeries_to_DataFrame)
    return Response_to_DataFrame

def Response_to_DataFrame_fn(TimeSeries_to_DataFrame: Callable) -> Callable[[str], pd.DataFrame]:

    def Response_to_DataFrame(response_text: str) -> pd.DataFrame:
        """
        """
        response_xml = drop_xml_encoding_line(response_text)
        root = etree.fromstring(response_xml)

        # get_response_timeinterval = lambda string: root.find(f'./period.timeInterval/{string}', root.nsmap).text
        # logging.info(f"Start: {get_response_timeinterval('start')}, End: {get_response_timeinterval('end')}")

        TimeSeries_list = root.findall("TimeSeries", root.nsmap)
        TimeSeries_dfs = map(TimeSeries_to_DataFrame, TimeSeries_list)
        df = pd.concat(TimeSeries_dfs, axis=0)
        return df

    return Response_to_DataFrame


def TimeSeries_to_DataFrame_fn(Period_to_DataFrame: Callable) -> Callable:

    def TimeSeries_to_DataFrame(TimeSeries: etree._Element) -> pd.DataFrame:
        # BIG TODO: 4.2.4. Flow-based Parameters [11.1.B] seems particularly convoluted.
        periods = TimeSeries.findall(".//Period", TimeSeries.nsmap)
        period_dfs = [Period_to_DataFrame(period) for period in periods]
        df = pd.concat(period_dfs, axis=0)
        [TimeSeries.remove(period) for period in periods]
        meta_df = pd.json_normalize(dict([unfold_node(TimeSeries)]))
        df = df.assign(**(meta_df.iloc[0].to_dict()))
        return df

    return TimeSeries_to_DataFrame


def unfold_node(node: etree._Element) -> tuple[str, dict[str, dict[str, ]]]:
    """
    Recursive unfolding of a node into a dict.
    TODO: Ensure no overwriting of same dict-names in the unfolding.
    """
    tag: str = node.tag.partition('}')[2]
    children: etree._Element = node.getchildren()
    if children == []:
        return (tag, node.text)
    else:
        return tag, dict([unfold_node(child) for child in children])


def Period_to_DataFrame_fn(get_Period_data: Callable) -> Callable:

    def Period_to_DataFrame(Period: etree._Element) -> pd.DataFrame:
        """
        Periods are implcitly valid as index is constructed independent from data extraction.
        Errors would occur at DataFrame construction.
        """
        index = get_Period_index(Period)
        data = get_Period_data(Period)
        df = pd.DataFrame(data=data, index=index)
        return df

    return Period_to_DataFrame


def get_Period_index(Period: etree._Element) -> pd.Index:
    start = Period.find("./timeInterval/start", Period.nsmap).text
    end = Period.find("./timeInterval/end", Period.nsmap).text
    resolution = Period.find("./resolution", Period.nsmap).text
    index = pd.date_range(start, end, freq=resolution_map[resolution])[:-1]
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
    points = Period.findall('.//Point', Period.nsmap)
    data = [dict((item.tag.partition('}')[2], item.text) for item in point) for point in points]
    return data
