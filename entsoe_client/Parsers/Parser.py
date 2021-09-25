from typing import List, Dict

from lxml import etree, objectify
import requests
import pandas as pd

from io import BytesIO
from zipfile import ZipFile

from entsoe_client.Parsers.Balacing_MarketDocument_Parser import Balancing_MarketDocument_Parser, \
    Balancing_MarketDocument_FinancialExpensesAndIncomeForBalancing_Parser
from entsoe_client.Parsers.GL_MarketDocument_Parser import GL_MarketDocument_Parser
from entsoe_client.Parsers.Publication_MarketDocument_Parser import Publication_MarketDocument_Parser
from entsoe_client.Parsers.TransmissionNetwork_MarketDocument_Parser import \
    TransmissionNetwork_MarketDocument_Parser

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
    def deserialize_xml(response_content: bytes) -> objectify.ObjectifiedElement:
        objectified_xml = objectify.fromstring(response_content)
        for elem in objectified_xml.getiterator():
            elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(objectified_xml)
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
