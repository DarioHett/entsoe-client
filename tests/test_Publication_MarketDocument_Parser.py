import unittest
from entsoe_client.Parsers import XMLParser, ParserFactory
import pandas as pd
import os

import entsoe_client.Parsers.Publication_MarketDocument_Parser


class test_Publication_MarketDocument_Parser(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        cls.response_contents: dict = {}
        path = "./tests/data/Publication_MarketDocument/"
        for file in os.listdir(path):
            with open(path+file, "rb") as data:
                cls.response_contents[file] = data.read()


    def test_dataloading(self):
        self.assertIsInstance(self.response_contents, dict)
        for i in range(len(self.response_contents)):
            with self.subTest(i=i):
                keys = list(self.response_contents.keys())
                values = list(self.response_contents.values())
                self.assertIsInstance(values[i], bytes)


    def test_factory_choice(self):
        types = ["A61"]
        for i in range(len(types)):
            with self.subTest(i=i):
                parser = ParserFactory.get_parser("Publication_MarketDocument", types[i])
                self.assertIsInstance(parser,
                                      entsoe_client.Parsers.Publication_MarketDocument_Parser.Publication_MarketDocument_Parser)


    def test_parse_basic(self):
        """Basic Query."""
        parser = XMLParser()
        keys = list(self.response_contents.keys())
        values = list(self.response_contents.values())
        df = parser.parse(values[0])
        self.assertIsInstance(df, pd.DataFrame)


    def test_parse_all(self):
        for file,content in self.response_contents.items():
            parser = XMLParser()
            df = parser.parse(content)
            self.assertIsInstance(df, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
