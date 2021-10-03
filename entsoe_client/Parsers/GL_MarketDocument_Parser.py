from entsoe_client.Parsers import ParserUtils as utils
from entsoe_client.Parsers.Entsoe_Document_Parser import Entsoe_Document_Parser


class Abstract_GL_MarketDocument_Parser(Entsoe_Document_Parser):
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


class GL_MarketDocument_Parser(Abstract_GL_MarketDocument_Parser):
    def __init__(self):
        super(GL_MarketDocument_Parser, self).__init__()
        self.set_Series_Period_Parser(utils.StandardPeriodParser)
        self.set_TimeSeries_Parser(
            utils.Tree_to_DataFrame(self.Series_Period_Parser, "Period")
        )
        self.set_Document_Parser(
            utils.Tree_to_DataFrame(self.TimeSeries_Parser, "TimeSeries")
        )

    def parse(self):
        return self.Document_Parser(self.objectified_input_xml)
