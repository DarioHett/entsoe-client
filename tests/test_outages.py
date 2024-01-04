import logging
import unittest

from pandas import DataFrame
from settings import *

from entsoe_client import Client
from entsoe_client.ParameterTypes import *
from entsoe_client.Parsers import Parser
from entsoe_client.Queries import Outages, Query


class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.queries = [
            # All unvailable.
            # Outages.UnavailabilityOfConsumptionUnits(
            #         biddingZone_Domain=Area('FR'),
            #         periodStart=202108240000,
            #         periodEnd = 202108250000
            # ),
            Outages.UnavailabilityOfGenerationUnits(
                biddingZone_Domain=Area("FR"),
                periodStart=202108240000,
                periodEnd=202108250000,
            ),
            Outages.UnavailabilityOfProductionUnits(
                biddingZone_Domain=Area("FR"),
                periodStart=202108240000,
                periodEnd=202108250000,
            ),
            Outages.UnavailabilityOfOffshoreGridInfrastructure(
                biddingZone_Domain=Area("DE_TENNET"),
                periodStart=202108010000,
                periodEnd=202108250000,
            ),
            Outages.UnavailabilityOfTransmissionInfrastructure(
                in_Domain=Area("DE_50HZ"),
                out_Domain=Area("PL_CZ"),
                periodStart=202108010000,
                periodEnd=202108250000,
            ),
        ]

    def test_integration(self):
        client = Client(api_key=api_key)
        self.assertIsInstance(client, Client)

        query = self.queries[0]
        self.assertIsInstance(query, Query)

        response = client.download(query)
        self.assertTrue(response.ok)

        # df = Parser.parse(response)
        # self.assertIsInstance(df, DataFrame)
        with self.assertRaises(NotImplementedError) as context:
            Parser.parse(response)

    def test_all(self):
        client = Client(api_key=api_key)
        for query in self.queries:
            with self.subTest(type(query).__name__):
                logging.debug(type(query).__name__)
                print(type(query).__name__)
                response = client.download(query)
                # df = Parser.parse(response)
                # self.assertIsInstance(df, DataFrame)
                with self.assertRaises(NotImplementedError) as context:
                    Parser.parse(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(verbosity=101)
