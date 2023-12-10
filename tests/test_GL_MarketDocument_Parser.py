import os
import unittest

import pandas as pd

import entsoe_client.Parsers.GL_MarketDocument_Parser
from entsoe_client.Parsers import Parser, ParserFactory, XMLParser, ZipParser


class test_GL_MarketDocument_Parser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.response_contents: list = []
        # path = "./tests/data/GL_MarketDocument/"
        # for file in os.listdir(path):
        #     with open(path + file, "rb") as data:
        #         cls.response_contents.append(data.read())

    def test_dataloading(self):
        self.assertIsInstance(self.response_contents, list)
        for i in range(len(self.response_contents)):
            with self.subTest(i=i):
                self.assertIsInstance(self.response_contents[i], bytes)

    def test_factory_choice(self):
        types = ["A65", "A70", "A71", "A72", "A73", "A68", "A69", "A74", "A75"]
        for i in range(len(types)):
            with self.subTest(i=i):
                parser = ParserFactory.get_parser("GL_MarketDocument", types[i])
                self.assertIsInstance(
                    parser,
                    entsoe_client.Parsers.GL_MarketDocument_Parser.GL_MarketDocument_Parser,
                )

    def test_parse_all(self):
        parser = XMLParser()
        for response_content in self.response_contents:
            df = parser.parse(response_content)
            self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
