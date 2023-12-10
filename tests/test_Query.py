import unittest

import entsoe_client
from entsoe_client.ParameterTypes import *


class QueryTest(unittest.TestCase):
    def test_set_periodStart(self):
        q = entsoe_client.Query(periodStart="2021-01-01T01:00:00")
        self.assertEqual(q.periodStart, 202101010100)

        q = entsoe_client.Queries.Load.DayAheadTotalLoad(
            outBiddingZone_Domain=Area("DE_LU"),
            periodStart="2021-01-01T01:00:00",
            periodEnd="2021-01-02T01:00:00",
        )
        self.assertEqual(q.periodStart, 202101010100)


if __name__ == "__main__":
    unittest.main(verbosity=101)
