from entsoe_client.Queries import Query
from entsoe_client.ParameterTypes import *
from typing import Union
import pandas as pd


class Generation(Query):
    """
    4.4. Generation domain
    For most of the data items in the generation domain,
    the PsrType parameter is optional. When this parameter is not used,
    API returns all available data for each production document_type for the queried interval and area.
    If the parameter is used, data will be returned only for the specific production document_type requested.
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
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        processType: ProcessType = None,
        psrType: PsrType = None,
        auctionCategory: AuctionCategory = None,
        update_DateAndOrTime=None,
        classificationSequence_AttributeInstanceComponent_Position: int = None,
        registeredResource=None,
    ):
        super(Generation, self).__init__(
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
            psrType=psrType,
            auctionCategory=auctionCategory,
            update_DateAndOrTime=update_DateAndOrTime,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
            registeredResource=registeredResource,
        )

    def __call__(self):
        return super(Generation, self).__call__()


class InstalledGenerationCapacityAggregated(Generation):
    """
    4.4.1. Installed Generation Capacity Aggregated [14.1.A]
    One year range limit applies
    Minimum time interval in query response is one year
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        PsrType (When used, only queried production document_type is returned)
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A33,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(InstalledGenerationCapacityAggregated, self).__init__(
            documentType=DocumentType.A68,
            processType=processType,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class InstalledGenerationCapacityPerUnit(Generation):
    """
    4.4.2. Installed Generation Capacity per Unit [14.1.B]
    One year range limit applies
    Minimum time interval in query response is one year
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        PsrType (When used, only queried production document_type is returned)
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A33,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(InstalledGenerationCapacityPerUnit, self).__init__(
            documentType=DocumentType.A71,
            processType=processType,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class DayAheadAggregatedGeneration(Generation):
    """
    4.4.3. Day-ahead Aggregated Generation [14.1.C]
    One year range limit applies
    Minimum time interval in query response is one day
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(DayAheadAggregatedGeneration, self).__init__(
            documentType=DocumentType.A71,
            processType=ProcessType.A01,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class DayAheadGenerationForecastsWindSolar(Generation):
    """
    4.4.4. Day-ahead Generation Forecasts for Wind and Solar [14.1.D]
        One year range limit applies
        Minimum time interval in query response is one day
        Mandatory parameters
            DocumentType
            ProcessType
            In_Domain
            TimeInterval or combination of PeriodStart and PeriodEnd
        Optional parameters
            PsrType (When used, only queried production document_type is returned)
    """

    def __init__(
        self,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(DayAheadGenerationForecastsWindSolar, self).__init__(
            documentType=DocumentType.A69,
            processType=ProcessType.A01,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class CurrentGenerationForecastsWindSolar(Generation):
    """
    4.4.5. Current Generation Forecasts for Wind and Solar [14.1.D]
    One year range limit applies
    Minimum time interval in query response is one day
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        PsrType (When used, only queried production document_type is returned)
    """

    def __init__(
        self,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(CurrentGenerationForecastsWindSolar, self).__init__(
            documentType=DocumentType.A69,
            processType=ProcessType.A18,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class IntradayGenerationForecastsWindSolar(Generation):
    """
    4.4.6. Intraday Generation Forecasts for Wind and Solar [14.1.D]
    One year range limit applies
    Minimum time interval in query response is one MTU period
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        PsrType (When used, only queried production document_type is returned)
    """

    def __init__(
        self,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(IntradayGenerationForecastsWindSolar, self).__init__(
            documentType=DocumentType.A69,
            processType=ProcessType.A40,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class ActualGenerationOutputPerGenerationUnit(Generation):
    """
    4.4.7. Actual Generation Output per Generation Unit [16.1.A]
    One day range limit applies
    Minimum time interval in query response is one MTU period
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain (can only be queried for Control Area EIC Code)
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        PsrType (When used, only queried production document_type is returned)
        RegisteredResource (EIC of Generation Unit)
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A16,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
        registeredResource=None,
    ):
        super(ActualGenerationOutputPerGenerationUnit, self).__init__(
            documentType=DocumentType.A73,
            processType=processType,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
            registeredResource=registeredResource,
        )


class AggregatedGenerationPerType(Generation):
    """
    4.4.8. Aggregated Generation per Type [16.1.B&C]
    One year range limit applies
    Minimum time interval in query response is one MTU period
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
         PsrType (When used, only queried production document_type is returned)
    Please note the followings:
    Response from API is same irrespective of querying for Document Types A74 - Wind & Solar;
    A75 - Actual  Generation Per Type.
    Time series with inBiddingZone_Domain attribute reflects Generation values,
    while outBiddingZone_Domain reflects Consumption values.
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A16,
        in_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        psrType: PsrType = None,
    ):
        super(AggregatedGenerationPerType, self).__init__(
            documentType=DocumentType.A75,
            processType=processType,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class AggregatedFillingRateOfWaterReservoirsAndHydroStoragePlants(Generation):
    """
    4.4.9. Aggregated Filling Rate of Water Reservoirs and Hydro Storage Plants [16.1.D]
    One year range limit applies
    Minimum time inteval in query response is one week
    Mandatory parameters
        DocumentType
        ProcessType
        In_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        in_Domain: Area = None,
        processType: ProcessType = ProcessType.A16,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
    ):
        super(
            AggregatedFillingRateOfWaterReservoirsAndHydroStoragePlants, self
        ).__init__(
            documentType=DocumentType.A72,
            processType=processType,
            in_Domain=in_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )
