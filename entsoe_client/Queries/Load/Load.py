from entsoe_client.Queries import Query
from entsoe_client.ParameterTypes import *
from typing import Dict, Union
import pandas as pd


class Load(Query):
    """4.1 Load domain."""

    def __init__(
        self,
        # documentType: DocumentType,
        processType: ProcessType = None,
        outBiddingZone_Domain: Area = None,
        periodStart: Union[str, pd.Timestamp] = None,
        periodEnd: Union[str, pd.Timestamp] = None,
    ):
        super(Load, self).__init__(
            documentType=DocumentType.A65,
            processType=processType,
            outBiddingZone_Domain=outBiddingZone_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class ActualTotalLoad(Load):
    """
    4.1.1. Actual Total Load [6.1.A]
    One year range limit applies
    Minimum time interval in query response_xml is one MTU Period
    Mandatory parameters
        DocumentType
        ProcessType
        OutBiddingZone_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd

    # q = ActualTotalLoad(Area.CZ, '201512312300', '201612312300')
    """

    def __init__(
        self,
        outBiddingZone_Domain: Area,
        periodStart: Union[str, pd.Timestamp],
        periodEnd: Union[str, pd.Timestamp],
    ):
        super(ActualTotalLoad, self).__init__(
            processType=ProcessType.A16,
            outBiddingZone_Domain=outBiddingZone_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class DayAheadTotalLoad(Load):
    """
    4.1.2. Day-Ahead Total Load Forecast [6.1.B]
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        ProcessType
        OutBiddingZone_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        outBiddingZone_Domain: Area,
        periodStart: Union[str, pd.Timestamp],
        periodEnd: Union[str, pd.Timestamp],
    ):
        super().__init__(ProcessType.A01, outBiddingZone_Domain, periodStart, periodEnd)

    def __call__(self) -> Dict:
        return super(DayAheadTotalLoad, self).__call__()


class WeekAheadTotalLoad(Load):
    """
    4.1.3. Week-Ahead Total Load Forecast [6.1.C]
    One year range limit applies
    Minimum time interval in query response_xml is one week
    Mandatory parameters
        DocumentType
        ProcessType
        OutBiddingZone_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        outBiddingZone_Domain: Area,
        periodStart: Union[str, pd.Timestamp],
        periodEnd: Union[str, pd.Timestamp],
    ):
        super().__init__(ProcessType.A31, outBiddingZone_Domain, periodStart, periodEnd)

    def __call__(self) -> Dict:
        return super(WeekAheadTotalLoad, self).__call__()


class MonthAheadTotalLoad(Load):
    """
    4.1.4. Month-Ahead Total Load Forecast [6.1.D]
    One year range limit applies
    Minimum time interval in query response_xml is one month
    Mandatory parameters
        DocumentType
        ProcessType
        OutBiddingZone_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        outBiddingZone_Domain: Area,
        periodStart: Union[str, pd.Timestamp],
        periodEnd: Union[str, pd.Timestamp],
    ):
        super().__init__(ProcessType.A32, outBiddingZone_Domain, periodStart, periodEnd)


class YearAheadTotalLoad(Load):
    """
    4.1.5. Year-Ahead Total Load Forecast [6.1.E]
    One year range limit applies
    Minimum time interval in query response_xml is one year
    Mandatory parameters
        DocumentType
        ProcessType
        OutBiddingZone_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        outBiddingZone_Domain: Area,
        periodStart: Union[str, pd.Timestamp],
        periodEnd: Union[str, pd.Timestamp],
    ):
        super().__init__(ProcessType.A33, outBiddingZone_Domain, periodStart, periodEnd)
