from entsoe_client.Parsers import ParserUtils as utils
from entsoe_client.Parsers.Entsoe_Document_Parser import Entsoe_Document_Parser

class Abstract_Acknowledgment_MarketDocument_Parser(Entsoe_Document_Parser):
    def __init__(self):
        super().__init__()
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


class Acknowledgment_MarketDocument_Parser(Abstract_Acknowledgment_MarketDocument_Parser):
    def __init__(self):
        super(Acknowledgment_MarketDocument_Parser, self).__init__()
        self.set_Document_Parser(utils.StandardErrorDocumentParser)

    def parse(self):
        df = self.Document_Parser(self.objectified_input_xml)
        # Make it easier for the user to read the error message by shuffling it to the top
        index = [df.index[0], df.index[-1], df.index[-2]]
        index.extend(df.index[1:-2])
        df = df.reindex(index=index)

        return df
