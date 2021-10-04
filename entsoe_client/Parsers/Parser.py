from io import BytesIO
from typing import List
from zipfile import ZipFile

import pandas as pd
import requests
from lxml import etree, objectify

from entsoe_client.Parsers.Balacing_MarketDocument_Parser import (
    Balancing_MarketDocument_Parser,
    Balancing_MarketDocument_FinancialExpensesAndIncomeForBalancing_Parser,
)
from entsoe_client.Parsers.GL_MarketDocument_Parser import GL_MarketDocument_Parser
from entsoe_client.Parsers.Publication_MarketDocument_Parser import (
    Publication_MarketDocument_Parser,
)
from entsoe_client.Parsers.TransmissionNetwork_MarketDocument_Parser import (
    TransmissionNetwork_MarketDocument_Parser,
)


class Parser:
    @staticmethod
    def parse(response: requests.Response):
        response_type = response.headers["Content-Type"]
        content = response.content
        if response_type == "text/xml":
            parser = XMLParser()
        elif response_type == "application/zip":
            parser = ZipParser()
        else:
            raise NotImplementedError
        df = parser.parse(content)
        return df

    def __call__(self, response: requests.Response):
        return self.parse(response)


class ZipParser:
    @staticmethod
    def unpack_archive(response_content: bytes) -> List[bytes]:
        archive = ZipFile(BytesIO(response_content), "r")
        xml_document_list = [archive.read(file) for file in archive.infolist()]
        return xml_document_list

    def parse(self, zip_archive: bytes):
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

    def parse(self, xml_document: bytes):
        object_content = self.deserialize_xml(xml_document)
        parser = factory.get_parser(object_content.tag, object_content.type.text)
        parser.set_objectified_input_xml(object_content)
        return parser.parse()


class ParserFactory:
    @staticmethod
    def get_parser(tag: str, document_type: str):
        if tag in ["GL_MarketDocument"]:
            if document_type in ["A65", "A70"]:  # Load
                return GL_MarketDocument_Parser()
            elif document_type in [
                "A71",
                "A72",
                "A73",
                "A68",
                "A69",
                "A74",
                "A75",
            ]:  # Generation
                return GL_MarketDocument_Parser()
            else:
                raise ValueError(document_type)
        elif tag in ["TransmissionNetwork_MarketDocument"]:
            if document_type in ["A90", "A63", "A91", "A92"]:
                return TransmissionNetwork_MarketDocument_Parser()
            else:
                raise ValueError(document_type)
        elif tag in ["Publication_MarketDocument"]:
            if document_type in [
                "A61",
                "A31",
                "A93",
                "A25",
                "A26",
                "A44",
                "A09",
                "A11",
                "A94",
            ]:
                return Publication_MarketDocument_Parser()
            else:
                raise ValueError(document_type)
        elif tag in ["Balancing_MarketDocument"]:
            if document_type in [
                "A81",
                "A82",
                "A83",
                "A84",
                "A88",
                "A89",
            ]:  # XML Responses
                return Balancing_MarketDocument_Parser()
            elif document_type in ["A85", "A86"]:  # Zip Responses
                return Balancing_MarketDocument_Parser()
            elif document_type in ["A87"]:  # Special "Point" Type.
                return (
                    Balancing_MarketDocument_FinancialExpensesAndIncomeForBalancing_Parser()
                )
            else:
                raise ValueError(document_type)
        else:
            raise NotImplementedError(tag)


factory = ParserFactory()
