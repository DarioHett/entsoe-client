from entsoe_client.Queries import Query
from entsoe_client.ParameterTypes import *
from typing import Dict, Union, Optional, Any
import pandas as pd


class Transmission(Query):
    """
    Parameters
        DocumentType
        Auction.Type
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
        Auction.Category
        Update_DateAndOrTime (For Offered Capacity Evolution can be quried with datetime in numeric.
        For example 20210803113900000 for evolution update date time 03.08.2021 13:39:00.000)
        ClassificationSequence_AttributeInstanceComponent.Position

    """

    def __init__(
        self,
        documentType: DocumentType = None,
        docStatus: DocStatus = None,
        auctionType: AuctionType = None,
        businessType: BusinessType = None,
        contract_MarketAgreementType: MarketAgreementType = None,
        in_Domain: Area = None,
        out_Domain: Area = None,
        periodStart: Union[int, str, int, pd.Timestamp] = None,
        periodEnd: Union[int, str, int, pd.Timestamp] = None,
        processType: ProcessType = None,
        auctionCategory: AuctionCategory = None,
        update_DateAndOrTime=None,
        classificationSequence_AttributeInstanceComponent_Position: int = None,
    ):
        super(Transmission, self).__init__(
            documentType=documentType,
            docStatus=docStatus,
            auctionType=auctionType,
            businessType=businessType,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            processType=processType,
            auctionCategory=auctionCategory,
            update_DateAndOrTime=update_DateAndOrTime,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
        )

    def __call__(self) -> Dict:
        _ = super(Transmission, self).__call__()
        _ = dict(
            ("classificationSequence_AttributeInstanceComponent.Position", v)
            if k == "classificationSequence_AttributeInstanceComponent_Position"
            else (k, v)
            for (k, v) in _.items()
        )
        _ = dict(
            ("contract_MarketAgreement.Type", v)
            if k == "contract_MarketAgreementType"
            else (k, v)
            for (k, v) in _.items()
        )
        _ = dict(
            ("auction.Type", v) if k == "auctionType" else (k, v)
            for (k, v) in _.items()
        )
        _ = dict(
            ("auction.Category", v) if k == "auctionCategory" else (k, v)
            for (k, v) in _.items()
        )
        return _


class ExpansionDismantlingProjects(Transmission):
    """
    4.2.1. Expansion and Dismantling Projects [9.1]
    100 documents limit applies
    Time interval in query response_xml depends on duration of matching projects
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        DocStatus

    TODO: ENTSO-E Documentation Example is wrong. Use SE3-SE4 in 2015.
    # q = ExpansionDismantlingProjects(in_Domain=Area.SE_3, out_Domain=Area.SE_4,
    #                                  periodStart='201412312300', periodEnd='201512312300',
    #                                  businessType=BusinessType.B01)
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
        businessType: Optional[BusinessType] = None,
        docStatus: Optional[DocStatus] = None,
    ):
        super(ExpansionDismantlingProjects, self).__init__(
            documentType=DocumentType("Interconnection network expansion"),
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            docStatus=docStatus,
        )


class ForecastedCapacity(Transmission):
    """
    4.2.2. Forecasted Capacity [11.1.A]
    One year range limit applies
    Minimum time interval in query response_xml ranges from day to year, depending on selected Contract_MarketAgreement.Type
    Mandatory parameters
        DocumentType
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd

    # q = ForecastedCapacity(contract_MarketAgreementType=MarketAgreementType.A01,
    #                        in_Domain=Area.CZ, out_Domain=Area.SK,
    #                        periodStart='201512312300', periodEnd='201612312300')
    """

    def __init__(
        self,
        marketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(ForecastedCapacity, self).__init__(
            documentType=DocumentType("Estimated Net Transfer Capacity"),
            contract_MarketAgreementType=marketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class OfferedCapacity(Transmission):
    """
    4.2.3. Offered Capacity [11.1.A]
    100 documents limit applies
    Minimum time interval in query response_xml ranges from part of day to year, depending on selected
    Contract_MarketAgreement.Type.
    Mandatory parameters
        DocumentType
        Auction.Type
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        Auction.Category
        Update_DateAndOrTime (For Offered Capacity Evolution can be quried with datetime in numeric.
        For example 20210803113900000 for evolution update date time 03.08.2021 13:39:00.000)
        ClassificationSequence_AttributeInstanceComponent.Position

    TODO:  Update_DateAndOrTime and ClassificationSequence_AttributeInstanceComponent.Position need verification.
    TODO: `quried` typo imported from original ENTSO-E documentation
    """

    def __init__(
        self,
        auctionType: AuctionType,
        contract_MarketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
        auctionCategory: Optional[AuctionCategory] = None,
        update_DateAndOrTime: Optional[int] = None,
        classificationSequence_AttributeInstanceComponent_Position: Optional[
            Any
        ] = None,
    ):
        super(OfferedCapacity, self).__init__(
            documentType=DocumentType.A31,
            auctionType=auctionType,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            auctionCategory=auctionCategory,
            update_DateAndOrTime=update_DateAndOrTime,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
        )

    def __call__(self) -> Dict:
        """
        Adjustment Required, keys: contract_MarketAgreementType -> contract_MarketAgreement.Type
        """
        return super(OfferedCapacity, self).__call__()


class FlowbasedParameters(Transmission):
    """
    4.2.4. Flow-based Parameters [11.1.B]
    100 documents limit applies
    Minimum time interval in query response_xml is one day for day-ahead allocations
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    In_Domain and Out_Domain must both contain the EIC code of the region

    # q = FlowbasedParameters(processType=ProcessType.A01, in_Domain=Area.CWE, out_Domain=Area.CWE,
    #                         periodStart='201512312300', periodEnd='201601012300')
    """

    def __init__(
        self,
        processType: ProcessType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(FlowbasedParameters, self).__init__(
            documentType=DocumentType.B11,
            processType=processType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class IntradayTransferLimits(Transmission):
    """
    4.2.5. Intraday Transfer Limits [11.3]
    One year range limit applies
    Minimum time interval in query response_xml ranges from part of day up to one day
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd

    # q = IntradayTransferLimits(in_Domain=Area.GB, out_Domain=Area.FR,
    #                         periodStart='201512312300', periodEnd='201601312300')
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(IntradayTransferLimits, self).__init__(
            documentType=DocumentType.A93,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class ExplicitAllocationInformationCapacity(Transmission):
    """
    4.2.6.Explicit Allocation Information(Capacity)[12.1.A]
    100 documents limit applies
    Minimum time interval in query response_xml ranges from part of day to year, depending on selected
    Contract_MarketAgreement.Type.
    Mandatory parameters
        DocumentType
        BusinessType
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        Auction.Category
        ClassificationSequence_AttributeInstanceComponent.Position

    # Example:
    https://transparency.entsoe.eu/transmission/r2/explicitAllocationsDayAhead/show?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime=01.01.2020+00:00|UTC|DAY&dateTime.endDateTime=02.01.2020+00:00|UTC|DAY&border.values=CTY|10Y1001A1001A83F!BZN_BZN|10Y1001A1001A82H_BZN_BZN|10YCH-SWISSGRIDZ&direction.values=Export&direction.values=Import&category.values=A01&category.values=A04&category.values=A03&category.values=A02&sequence.values=1&sequence.values=2&sequence.values=3&sequence.values=4&sequence.values=5&sequence.values=6&dv-datatable_length=10
    query = Queries.Transmission.ExplicitAllocationInformationCapacity(
        periodStart= 202001012300, periodEnd=202001022300, contract_MarketAgreementType=MarketAgreementType.A01,
        in_Domain=Area.CH, out_Domain=Area.DE_LU, auctionCategory=AuctionCategory.A01,
        classificationSequence_AttributeInstanceComponent_Position=1)
    """

    def __init__(
        self,
        contract_MarketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
        auctionCategory: Optional[AuctionCategory] = None,
        classificationSequence_AttributeInstanceComponent_Position=None,
    ):
        super(ExplicitAllocationInformationCapacity, self).__init__(
            documentType=DocumentType.A25,
            businessType=BusinessType.B05,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            auctionCategory=auctionCategory,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
        )


class ExplicitAllocationInformationRevenueonly(Transmission):
    """
    4.2.7. Explicit Allocation Information (Revenue only) [12.1.A]
    100 documents limit applies
    Minimum time interval in query response_xml ranges from part of day to year, depending on selected
    Contract_MarketAgreement.Type.
    Mandatory parameters
        DocumentType
        BusinessType
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd

    # q = ExplicitAllocationInformationRevenueonly(contract_MarketAgreementType=MarketAgreementType.A01,
    #                                              in_Domain=Area.AT, out_Domain=Area.CZ,
    #                                              periodStart='201601012300', periodEnd='201601022300'
    #                                              )
    """

    def __init__(
        self,
        contract_MarketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(ExplicitAllocationInformationRevenueonly, self).__init__(
            documentType=DocumentType.A25,
            businessType=BusinessType.B07,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class TotalCapacityNominated(Transmission):
    """
    4.2.8. Total Capacity Nominated [12.1.B]
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        BusinessType
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
        super(TotalCapacityNominated, self).__init__(
            documentType=DocumentType.A26,
            businessType=BusinessType.B08,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class TotalCapacityAlreadyAllocated(Transmission):
    """
    4.2.9. Total Capacity Already Allocated [12.1.C]
    100 documents limit applies
    Minimum time interval in query response_xml ranges from part of day to year,
    depending on selected Contract_MarketAgreement.Type
    Mandatory parameters
        DocumentType
        BusinessType
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional
        Auction.Category
    """

    def __init__(
        self,
        contract_MarketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(TotalCapacityAlreadyAllocated, self).__init__(
            documentType=DocumentType.A26,
            businessType=BusinessType.A29,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class DayAheadPrices(Transmission):
    """
    4.2.10. Day Ahead Prices [12.1.D]
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    In_Domain and Out_Domain must be populated with the same area EIC code
    """

    def __init__(
        self,
        in_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(DayAheadPrices, self).__init__(
            documentType=DocumentType.A44,
            in_Domain=in_Domain,
            out_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )
        assert self.in_Domain == self.in_Domain


class ImplicitAuctionNetPositions(Transmission):
    """
    4.2.12. Implicit Auction—Congestion Income [12.1.E]
    100 documents limit applies
    Minimum time interval in query response_xml ranges from part of day to one day,
    depending on selected Contract_MarketAgreement.Type
    Mandatory parameters
        DocumentType
        BusinessType
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    For implicit allocations, In_Domain and Out_Domain must be populated with the same border EIC code. For flow-based,
    they must be populated with the same bidding zone EIC code
    """

    def __init__(
        self,
        contract_MarketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(ImplicitAuctionNetPositions, self).__init__(
            documentType=DocumentType.A25,
            businessType=BusinessType.B09,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class ImplicitAuctionCongestionIncome(Transmission):
    """
    4.2.11. Implicit Auction—Net Positions [12.1.E]
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        BusinessType
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    In_Domain and Out_Domain must be populated with the same bidding zone EIC code
    """

    def __init__(
        self,
        contract_MarketAgreementType: MarketAgreementType,
        in_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(ImplicitAuctionCongestionIncome, self).__init__(
            documentType=DocumentType.A25,
            businessType=BusinessType.B10,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )
        assert self.in_Domain == self.out_Domain


class CommercialSchedules(Transmission):
    """
    (Custom class; leaving contract document_type unspecified w/o invoking a superclass.)
    4.2.13.1 Commercial Schedules
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        Contract Type
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
        contract_MarketAgreementType: MarketAgreementType,
    ):
        super(CommercialSchedules, self).__init__(
            documentType=DocumentType.A09,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            contract_MarketAgreementType=contract_MarketAgreementType,
        )


class TotalCommercialSchedules(Transmission):
    """
    4.2.13. Total Commercial Schedules [12.1.F]
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        Contract Type (A05)
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(TotalCommercialSchedules, self).__init__(
            documentType=DocumentType.A09,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            contract_MarketAgreementType=MarketAgreementType.A05,
        )


class DayAheadCommercialSchedules(Transmission):
    """
    4.2.14. Day-ahead Commercial Schedules [12.1.F]
    One year range limit applies
    Minimum time interval in query response_xml is one day
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        Contract Type (A01)
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(DayAheadCommercialSchedules, self).__init__(
            documentType=DocumentType.A09,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            contract_MarketAgreementType=MarketAgreementType.A01,
        )


class PhysicalFlows(Transmission):
    """
    4.2.15. Physical Flows [12.1.G]
    One year range limit applies
    Minimum time interval in query response_xml is MTU Period
    Mandatory parameters
        DocumentType
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Unlike Web GUI, API responds not netted values as data is requested per direction.
    """

    def __init__(
        self,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
    ):
        super(PhysicalFlows, self).__init__(
            documentType=DocumentType.A11,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class CapacityAllocatedOutsideEU(Transmission):
    """
    4.2.16. Capacity Allocated Outside EU [12.1.H]
    100 documents limit applies
    Minimum time interval in query response_xml ranges from part of day to year, depending on selected Contract_MarketAgreement.Type
    Mandatory parameters
        DocumentType
        Auction.Type
        Contract_MarketAgreement.Type
        In_Domain
        Out_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        Auction.Category
        ClassificationSequence_AttributeInstanceComponent.Position
    """

    def __init__(
        self,
        auctionType: AuctionType,
        marketAgreementType: MarketAgreementType,
        in_Domain: Area,
        out_Domain: Area,
        periodStart: Union[int, str, pd.Timestamp],
        periodEnd: Union[int, str, pd.Timestamp],
        auctionCategory: AuctionCategory,
        classificationSequence_AttributeInstanceComponent_Position: int,
    ):
        super(CapacityAllocatedOutsideEU, self).__init__(
            documentType=DocumentType("Non EU allocations"),
            contract_MarketAgreementType=marketAgreementType,
            auctionType=auctionType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            auctionCategory=auctionCategory,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
        )
