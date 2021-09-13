import unittest
import entsoe_client.Parser as Parser
import pandas as pd
import os


class test_Balancing_MarketDocument_Parser(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        cls.response_contents: dict = {}
        path = "./tests/data/Balancing_MarketDocument/"
        for file in os.listdir(path):
            with open(path+file, "rb") as data:
                cls.response_contents[file] = data.read()


    def test_dataloading(self):
        self.assertIsInstance(self.response_contents, dict)
        for i in range(len(self.response_contents)):
            with self.subTest(i=i):
                keys = list(self.response_contents.keys())
                values = list(self.response_contents.values())
                print(keys[i])
                self.assertIsInstance(values[i], bytes)


    def test_factory_choice(self):
        types = ["A81"]
        for i in range(len(types)):
            with self.subTest(i=i):
                parser = Parser.ParserFactory.get_parser("Balancing_MarketDocument", types[i])
                self.assertIsInstance(parser, Parser.Balancing_MarketDocument_Parser)


    def test_parse_basic(self):
        """Basic AmountOfBalancingReservesUnderContract Query."""
        parser = Parser.XMLParser()
        keys = list(self.response_contents.keys())
        values = list(self.response_contents.values())
        print(keys[-1])
        df = parser.parse(values[-1])
        self.assertIsInstance(df, pd.DataFrame)


    def test_parse_all(self):
        parser = Parser.XMLParser()
        for file,content in self.response_contents.items():
            print(file)
            df = parser.parse(content)
            self.assertIsInstance(df, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
