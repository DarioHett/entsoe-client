import pandas as pd

from entsoe_client.ParameterTypes import *
from typing import Dict, Any, Union
from pandas import Timestamp


class Query:
    """
    Base Class.
    Exhaustive parameter list.
    """

    def __init__(
        self,
        documentType: DocumentType = None,
        docStatus: DocStatus = None,
        processType: ProcessType = None,
        businessType: BusinessType = None,
        psrType: PsrType = None,
        type_MarketAgreementType: MarketAgreementType = None,
        contract_MarketAgreementType: MarketAgreementType = None,
        auctionType: AuctionType = None,
        auctionCategory: AuctionCategory = None,
        classificationSequence_AttributeInstanceComponent_Position: int = None,
        outBiddingZone_Domain: Area = None,
        biddingZone_Domain: Area = None,
        controlArea_Domain: Area = None,
        in_Domain: Area = None,
        out_Domain: Area = None,
        Acquiring_Domain: Area = None,
        Connecting_Domain: Area = None,
        registeredResource=None,
        timeInterval=None,
        periodStart=None,
        periodEnd=None,
        timeIntervalUpdate=None,
        periodStartUpdate=None,
        periodEndUpdate=None,
        update_DateAndOrTime=None,
        implementation_DateAndOrTime=None,  # Does not appear in Documentation; MasterData.
        Area_Domain=None,  # Does not appear in documentation.
        offset=None,
        mRID=None,
    ):
        """
        Appendix A: Complete parameter list
        A.1.Available parameters
        """
        self.documentType = documentType
        self.docStatus = docStatus
        self.processType = processType
        self.businessType = businessType
        self.psrType = psrType
        self.type_MarketAgreementType = type_MarketAgreementType
        self.contract_MarketAgreementType = contract_MarketAgreementType
        self.auctionType = auctionType
        self.auctionCategory = auctionCategory
        self.classificationSequence_AttributeInstanceComponent_Position = (
            classificationSequence_AttributeInstanceComponent_Position
        )
        self.outBiddingZone_Domain = outBiddingZone_Domain
        self.biddingZone_Domain = biddingZone_Domain
        self.controlArea_Domain = controlArea_Domain
        self.in_Domain = in_Domain
        self.out_Domain = out_Domain
        self.Acquiring_Domain = Acquiring_Domain
        self.Connecting_Domain = Connecting_Domain
        self.registeredResource = registeredResource
        self.timeInterval = timeInterval
        self.periodStart = self.datetime_parser(periodStart)
        self.periodEnd = self.datetime_parser(periodEnd)
        self.timeIntervalUpdate = timeIntervalUpdate
        self.periodStartUpdate = periodStartUpdate
        self.periodEndUpdate = periodEndUpdate
        self.update_DateAndOrTime = update_DateAndOrTime
        self.Area_Domain = Area_Domain
        self.implementation_DateAndOrTime = implementation_DateAndOrTime
        self.offset = offset
        self.mRID = mRID

    @staticmethod
    def datetime_parser(dateformat: Union[str, int, Timestamp]) -> int:
        fmt = "%Y%m%d%H%M"
        if isinstance(dateformat, Timestamp):
            return int(dateformat.strftime(fmt))
        if isinstance(dateformat, str):
            new_dateformat: Timestamp = pd.to_datetime(
                dateformat, infer_datetime_format=True, utc=True
            )
            return Query.datetime_parser(new_dateformat)
        if isinstance(dateformat, int):
            return dateformat

    def __call__(self) -> Dict:
        _ = self.__dict__
        _ = dict(
            (self.property_to_parameter(k), self.get_value_switch(v))
            for (k, v) in _.items()
        )
        return _

    @staticmethod
    def property_to_parameter(key: str):
        if key == "type_MarketAgreementType":
            return "type_MarketAgreement.Type"
        elif key == "contract_MarketAgreementType":
            return "contract_MarketAgreement.Type"
        else:
            return key

    @staticmethod
    def get_value_switch(parameter: Any):
        if type(parameter) in [
            Area,
            AuctionCategory,
            AuctionType,
            BusinessType,
            DocStatus,
            DocumentType,
            MarketAgreementType,
            ProcessType,
            PsrType,
        ]:
            return parameter.name
        else:
            return parameter
