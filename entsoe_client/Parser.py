from typing import List, Dict, Tuple

import lxml.objectify
import requests
import pandas as pd
import entsoe_client.ParserUtils as utils
from abc import ABC, abstractmethod

from io import BytesIO
from zipfile import ZipFile

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

# TODO: Implement `Parser` class which dynamically chooses Zip or XML.

class Parser:
    @staticmethod
    def parse(response: requests.Response):
        response_type = response.headers['Content-Type']
        content = response.content
        if response_type == 'text/xml':
            parser = XMLParser()
        elif response_type == 'application/zip':
            parser = ZipParser()
        else:
            raise NotImplementedError
        df = parser.parse(content)
        return df

class ZipParser:
    @staticmethod
    def unpack_archive(response_content: bytes) -> List[bytes]:
        archive = ZipFile(BytesIO(response_content), 'r')
        xml_document_list = [archive.read(file) for file in archive.infolist()]
        return xml_document_list

    # May change later to handle `Requests.response` types directly.
    def parse(self, zip_archive: bytes):
        # TODO: Now can only handle XML input; reshuffle later to handle other input (e.g. ZIP built from XML).
        parser = XMLParser()
        xml_documents = self.unpack_archive(zip_archive)
        dfs = [parser.parse(xml_document) for xml_document in xml_documents]
        df = pd.concat(dfs, axis=0)
        return df


class XMLParser:
    @staticmethod
    def deserialize_xml(response_content: bytes) -> lxml.objectify.ObjectifiedElement:
        objectified_xml = lxml.objectify.fromstring(response_content)
        for elem in objectified_xml.getiterator():
            elem.tag = lxml.etree.QName(elem).localname
        lxml.etree.cleanup_namespaces(objectified_xml)
        return objectified_xml

    # May change later to handle `Requests.response` types directly.
    def parse(self, xml_document: bytes):
        # TODO: Now can only handle XML input; reshuffle later to handle other input (e.g. ZIP built from XML).
        object_content = self.deserialize_xml(xml_document)
        parser = factory.get_parser(object_content.tag, object_content.type.text)
        parser.set_objectified_input_xml(object_content)
        return parser.parse()


class ParserFactory:
    @staticmethod
    def get_parser(tag: str, type: str):
        if tag in ["GL_MarketDocument"]:
            if type in ["A65", "A70"]: # Load
                return GL_MarketDocument_Parser()
            elif type in ["A71", "A72", "A73", "A68", "A69", "A74", "A75"]: # Generation
                return GL_MarketDocument_Parser()
            else:
                raise ValueError(type)
        elif tag in ["TransmissionNetwork_MarketDocument"]:
            if type in ["A90", "A63", "A91", "A92"]:
                return TransmissionNetwork_MarketDocument_Parser()
            else:
                raise ValueError(type)
        elif tag in ["Publication_MarketDocument"]:
            if type in ["A61", "A31", "A93", "A25", "A26", "A44", "A09", "A11", "A94"]:
                return Publication_MarketDocument_Parser()
            else:
                raise ValueError(type)
        elif tag in ["Balancing_MarketDocument"]:
            if type in ["A81", "A82", "A83", "A84", "A88", "A89"]: # XML Responses
                return Balancing_MarketDocument_Parser()
            elif type in ["A85", "A86"]: # Zip Responses
                return Balancing_MarketDocument_Parser()
            elif type in ["A87"]: # Special "Point" Type.
                return Balancing_MarketDocument_FinancialExpensesAndIncomeForBalancing_Parser()
            else:
                raise ValueError(type)
        else:
            raise ValueError(tag)


factory = ParserFactory()


class Entsoe_Document_Parser(ABC):
    def __init__(self):
        self.objectified_input_xml = None

    def set_objectified_input_xml(self, objectified_input_xml):
        self.objectified_input_xml = objectified_input_xml

    @classmethod
    @abstractmethod
    def parse(self):
        pass


class Abstract_GL_MarketDocument_Parser(Entsoe_Document_Parser):
    def __init__(self):
        self.Document_Parser = None
        self.TimeSeries_Parser = None
        self.Series_Period_Parser = None
        self.Point_Parser = None
        self.MktPSRType_Parser = None
        self.MktGeneratingUnit_Parser = None

    def set_Document_Parser(self, Document_Parser):
        self.Document_Parser = Document_Parser

    def set_TimeSeries_Parser(self, TimeSeries_Parser):
        self.TimeSeries_Parser = TimeSeries_Parser

    def set_Series_Period_Parser(self, Series_Period_Parser):
        self.Series_Period_Parser = Series_Period_Parser

    def set_Point_Parser(self, Point_Parser):
        self.Point_Parser = Point_Parser

    def set_MktPSRType_Parser(self, MktPSRType_Parser):
        self.MktPSRType_Parser = MktPSRType_Parser

    def set_MktGeneratingUnit_Parser(self, MktGeneratingUnit_Parser):
        self.MktGeneratingUnit_Parser = MktGeneratingUnit_Parser


class GL_MarketDocument_Parser(Abstract_GL_MarketDocument_Parser):
    def __init__(self):
        super(GL_MarketDocument_Parser, self).__init__()
        self.set_Series_Period_Parser(utils.StandardPeriodParser)
        self.set_TimeSeries_Parser(utils.Tree_to_DataFrame(self.Series_Period_Parser, 'Period'))
        self.set_Document_Parser(utils.Tree_to_DataFrame(self.TimeSeries_Parser, 'TimeSeries'))


    def parse(self):
        return self.Document_Parser(self.objectified_input_xml)


class Abstract_Publication_MarketDocument_Parser(Entsoe_Document_Parser):
    def __init__(self):
        self.Document_Parser = None
        self.TimeSeries_Parser = None
        self.Series_Period_Parser = None
        self.Point_Parser = None
        self.MktPSRType_Parser = None
        self.MktGeneratingUnit_Parser = None

    def set_Document_Parser(self, Document_Parser):
        self.Document_Parser = Document_Parser

    def set_TimeSeries_Parser(self, TimeSeries_Parser):
        self.TimeSeries_Parser = TimeSeries_Parser

    def set_Series_Period_Parser(self, Series_Period_Parser):
        self.Series_Period_Parser = Series_Period_Parser

    def set_Point_Parser(self, Point_Parser):
        self.Point_Parser = Point_Parser

    def set_MktPSRType_Parser(self, MktPSRType_Parser):
        self.MktPSRType_Parser = MktPSRType_Parser

    def set_MktGeneratingUnit_Parser(self, MktGeneratingUnit_Parser):
        self.MktGeneratingUnit_Parser = MktGeneratingUnit_Parser


class Publication_MarketDocument_Parser(Abstract_Publication_MarketDocument_Parser):
    def __init__(self):
        super(Publication_MarketDocument_Parser, self).__init__()
        self.set_Series_Period_Parser(utils.StandardPeriodParser)
        self.set_TimeSeries_Parser(utils.Tree_to_DataFrame(self.Series_Period_Parser, 'Period'))
        self.set_Document_Parser(utils.Tree_to_DataFrame(self.TimeSeries_Parser, 'TimeSeries'))

    def parse(self):
        return self.Document_Parser(self.objectified_input_xml)


class Abstract_TransmissionNetwork_MarketDocument_Parser(Entsoe_Document_Parser):
    def __init__(self):
        self.Document_Parser = None
        self.TimeSeries_Parser = None
        self.Series_Period_Parser = None
        self.Point_Parser = None
        self.MktPSRType_Parser = None
        self.MktGeneratingUnit_Parser = None

    def set_Document_Parser(self, Document_Parser):
        self.Document_Parser = Document_Parser

    def set_TimeSeries_Parser(self, TimeSeries_Parser):
        self.TimeSeries_Parser = TimeSeries_Parser

    def set_Series_Period_Parser(self, Series_Period_Parser):
        self.Series_Period_Parser = Series_Period_Parser

    def set_Point_Parser(self, Point_Parser):
        self.Point_Parser = Point_Parser

    def set_MktPSRType_Parser(self, MktPSRType_Parser):
        self.MktPSRType_Parser = MktPSRType_Parser

    def set_MktGeneratingUnit_Parser(self, MktGeneratingUnit_Parser):
        self.MktGeneratingUnit_Parser = MktGeneratingUnit_Parser


class TransmissionNetwork_MarketDocument_Parser(Abstract_TransmissionNetwork_MarketDocument_Parser):
    def __init__(self):
        super(TransmissionNetwork_MarketDocument_Parser, self).__init__()
        self.set_Series_Period_Parser(utils.StandardPeriodParser)
        self.set_TimeSeries_Parser(utils.Tree_to_DataFrame(self.Series_Period_Parser, 'Period'))
        self.set_Document_Parser(utils.Tree_to_DataFrame(self.TimeSeries_Parser, 'TimeSeries'))


    def parse(self):
        return self.Document_Parser(self.objectified_input_xml)

class Abstract_Balancing_MarketDocument_Parser(Entsoe_Document_Parser):
    def __init__(self):
        self.Document_Parser = None
        self.TimeSeries_Parser = None
        self.Series_Period_Parser = None
        self.Point_Parser = None
        self.MktPSRType_Parser = None
        self.MktGeneratingUnit_Parser = None


    def set_Document_Parser(self, Document_Parser):
        self.Document_Parser = Document_Parser

    def set_TimeSeries_Parser(self, TimeSeries_Parser):
        self.TimeSeries_Parser = TimeSeries_Parser

    def set_Series_Period_Parser(self, Series_Period_Parser):
        self.Series_Period_Parser = Series_Period_Parser

    def set_Point_Parser(self, Point_Parser):
        self.Point_Parser = Point_Parser

    def set_MktPSRType_Parser(self, MktPSRType_Parser):
        self.MktPSRType_Parser = MktPSRType_Parser

    def set_MktGeneratingUnit_Parser(self, MktGeneratingUnit_Parser):
        self.MktGeneratingUnit_Parser = MktGeneratingUnit_Parser


class Balancing_MarketDocument_Parser(Abstract_Balancing_MarketDocument_Parser):
    def __init__(self):
        super(Balancing_MarketDocument_Parser, self).__init__()
        self.set_Series_Period_Parser(utils.StandardPeriodParser)
        self.set_TimeSeries_Parser(utils.Tree_to_DataFrame(self.Series_Period_Parser, 'Period'))
        self.set_Document_Parser(utils.Tree_to_DataFrame(self.TimeSeries_Parser, 'TimeSeries'))


    def parse(self):
        return self.Document_Parser(self.objectified_input_xml)

class Balancing_MarketDocument_FinancialExpensesAndIncomeForBalancing_Parser(Abstract_Balancing_MarketDocument_Parser):
    def __init__(self):
        super(Balancing_MarketDocument_FinancialExpensesAndIncomeForBalancing_Parser, self).__init__()
        self.set_Series_Period_Parser(utils.Period_to_DataFrame_fn(utils.get_Period_Financial_Price_data))
        self.set_TimeSeries_Parser(utils.Tree_to_DataFrame(self.Series_Period_Parser, 'Period'))
        self.set_Document_Parser(utils.Tree_to_DataFrame(self.TimeSeries_Parser, 'TimeSeries'))


    def parse(self):
        return self.Document_Parser(self.objectified_input_xml)

def parse_bytes(response: requests.Response) -> lxml.objectify.ObjectifiedElement:
    object = lxml.objectify.fromstring(response.content)
    for elem in object.getiterator():
        elem.tag = lxml.etree.QName(elem).localname
    lxml.etree.cleanup_namespaces(object)
    return object


def parse_node(node: lxml.objectify.ObjectifiedElement, data_tag: str
               ) -> Tuple[Dict[str, str], List[lxml.objectify.ObjectifiedElement]]:
    metadata: dict = extract_metadata(node, f'{data_tag}')
    data: list = node.xpath(f'./{data_tag}')
    return metadata, data


def main(response):
    ### Save some memory.
    a = parse_bytes(response)
    metadata_0, data_0 = parse_node(a, 'TimeSeries')
    data_1 = [parse_node(data, 'Period') for data in data_0]
    pd.DataFrame([parse_node(pt, 'LOL')[0] for pt in [parse_node(data, 'Point') for data in data_1[4][1]][0][1]])
    # Now just unpack, attach the metadata and concatenate.


def extract_metadata(node: lxml.objectify.ObjectifiedElement, data_tag: str):
    subnodes = node.xpath(f"./*[not(self::{data_tag})]")
    unfolded_dict = dict(map(recursive_dict, subnodes))
    metadata: dict = flatten_dict({node.tag: unfolded_dict})
    return metadata


def recursive_dict(element):
    return element.tag, dict(map(recursive_dict, element.getchildren())) or element.text


def flatten_dict(d):
    def expand(key, value):
        if isinstance(value, dict):
            return [(key + '.' + k, v) for k, v in flatten_dict(value).items()]
        else:
            return [(key, value)]

    items = [item for k, v in d.items() for item in expand(k, v)]

    return dict(items)


def parse2(response: requests.Response) -> pd.DataFrame:
    tree = parse_bytes(response.content)
    if tree.tag == 'GL_MarketDocument':
        df = parse_gl_marketdocument(tree)
        return df
    else:
        raise NotImplementedError


def parse(response: requests.Response) -> pd.DataFrame:
    """
    Primary function to parse raw Responses to Pandas DataFrames.
    Switch-case functionality for different response content-types.
    TODO: Implement as a class; Factory for Content-Types.
    TODO: Handle successful but empty response.
    """
    content = response.headers.get('Content-Type', None)

    if content == 'application/xml':
        raise NotImplementedError
    elif 'documentType=A95' in response.url:
        return utils.parse_masterdata(response)
    elif 'documentType=A76' in response.url:
        return utils.parse_outages(response)
    elif 'documentType=A77' in response.url:
        return utils.parse_outages(response)
    elif 'documentType=A78' in response.url:
        return utils.parse_outages(response)
    elif 'documentType=A79' in response.url:
        return utils.parse_outages(response)
    elif 'documentType=A80' in response.url:
        return utils.parse_outages(response)
    elif 'documentType=B11' in response.url:
        return utils.parse_flowbasedparameters(response)
    elif content == 'application/zip':
        return utils.parse_zip(response)
    elif content == 'text/xml':
        return utils.parse_text_xml(response)
    elif content == 'text/xml':
        return utils.parse_text_xml(response)
    else:
        raise NotImplementedError
