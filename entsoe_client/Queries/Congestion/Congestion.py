from typing import Union

import pandas as pd

from entsoe_client.ParameterTypes import *
from entsoe_client.Queries import Query


class Congestion(Query):
    """4.3 Congestion domain."""

    def __init__(
        self,
        documentType: DocumentType = None,
        businessType: BusinessType = None,
        in_Domain: Area = None,
        out_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
    ):
        super(Congestion, self).__init__(
            documentType=documentType,
            businessType=businessType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class Redispatching(Congestion):
    """
    4.3.1. Redispatching [13.1.A]
    100 documents limit applies
    Time interval in query response depends on duration of matching redispatches
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(Redispatching, self).__init__(
            documentType=DocumentType.A63,
            businessType=BusinessType.A46,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class Countertrading(Congestion):
    """
    4.3.2. Countertrading [13.1.B]
    100 documents limit applies
    Time interval in query response depends on duration of matching counter trades
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(Countertrading, self).__init__(
            documentType=DocumentType("Counter trade notice"),
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class CostsOfCongestionManagement(Congestion):
    """
    4.3.3. Costs of Congestion Management [13.1.C]
    100 documents limit applies
    Minimum time interval in query response is one month
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
    In_Domain and Out_Domain must be populated with the same area EIC code.
    """

    def __init__(
        self,
        in_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(CostsOfCongestionManagement, self).__init__(
            documentType=DocumentType.A92,
            businessType=BusinessType.B03,
            in_Domain=in_Domain,
            out_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )
