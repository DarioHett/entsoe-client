import logging
import unittest

from pandas import DataFrame

from entsoe_client import Client
from entsoe_client.Parsers import Parser
from entsoe_client.Queries import Generation, Query
from entsoe_client.ParameterTypes import *
from settings import *


class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.queries = [
            Generation.InstalledGenerationCapacityAggregated(
                processType=ProcessType.A33,
                psrType=PsrType.B16,
                in_Domain=Area.CZ,
                periodStart=201512312300,
                periodEnd=201612312300
            ),
            Generation.InstalledGenerationCapacityPerUnit(
                processType=ProcessType.A33,
                psrType=PsrType.B02,
                in_Domain=Area.CZ,
                periodStart=201512312300,
                periodEnd=201612312300
            ),
            Generation.DayAheadAggregatedGeneration(
                in_Domain=Area.CZ,
                periodStart=201512312300,
                periodEnd=201612312300
            ),
            Generation.DayAheadGenerationForecastsWindSolar(
                in_Domain=Area.CZ,
                periodStart=201512312300,
                periodEnd=201612312300,
                psrType=PsrType.B16
            ),
            Generation.CurrentGenerationForecastsWindSolar(
                in_Domain=Area.BE,
                periodStart=201912312300,
                periodEnd=202012312300,
                psrType=PsrType.B16
            ),
            Generation.IntradayGenerationForecastsWindSolar(
                in_Domain=Area.DE_AT_LU,
                periodStart=201512312300,
                periodEnd=201612312300,
                psrType=PsrType.B16
            ),
            Generation.ActualGenerationOutputPerGenerationUnit(
                processType=ProcessType.A16,
                in_Domain=Area.BE,
                periodStart=202012302300,
                periodEnd=202012312300
            ),
            Generation.AggregatedGenerationPerType(
                in_Domain=Area.DE_LU,
                periodStart=202012310000,
                periodEnd=202012312300,
                psrType=PsrType.B02
            ),
            Generation.AggregatedFillingRateOfWaterReservoirsAndHydroStoragePlants(
                in_Domain=Area.NO_1,
                periodStart=201512312300,
                periodEnd=201612312300
            )
        ]

    def test_integration(self):
        client = Client(api_key=api_key)
        self.assertIsInstance(client, Client)

        query = self.queries[0]
        self.assertIsInstance(query, Query)

        response = client.download(query)
        self.assertTrue(response.ok)

        df = Parser.parse(response)
        self.assertIsInstance(df, DataFrame)

    def test_all(self):
        client = Client(api_key=api_key)
        for query in self.queries:
            with self.subTest(type(query).__name__):
                response = client.download(query)
                df = Parser.parse(response)
                self.assertIsInstance(df, DataFrame)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(verbosity=101)
