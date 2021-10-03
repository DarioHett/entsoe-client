from typing import Union
import pandas as pd
from entsoe_client.ParameterTypes import *
from entsoe_client.Queries import Query


class MasterData(Query):
    """4.3 Congestion domain."""

    def __init__(
        self,
        documentType: DocumentType = None,
        docStatus: DocStatus = None,
        auctionType: AuctionType = None,
        businessType: BusinessType = None,
        psrType: PsrType = None,
        contract_MarketAgreementType: MarketAgreementType = None,
        in_Domain: Area = None,
        out_Domain: Area = None,
        periodStart: Union[str, int, pd.Timestamp] = None,
        periodEnd: Union[str, int, pd.Timestamp] = None,
        processType: ProcessType = None,
        auctionCategory: AuctionCategory = None,
        update_DateAndOrTime=None,
        biddingZone_Domain=None,
        implementation_DateAndOrTime: str = None,
        classificationSequence_AttributeInstanceComponent_Position: int = None,
    ):
        super(MasterData, self).__init__(
            documentType=documentType,
            docStatus=docStatus,
            auctionType=auctionType,
            businessType=businessType,
            psrType=psrType,
            contract_MarketAgreementType=contract_MarketAgreementType,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            biddingZone_Domain=biddingZone_Domain,
            periodEnd=periodEnd,
            processType=processType,
            auctionCategory=auctionCategory,
            update_DateAndOrTime=update_DateAndOrTime,
            implementation_DateAndOrTime=implementation_DateAndOrTime,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
        )


class ProductionAndGenerationUnits(MasterData):
    """
    4.5.1. Production and Generation Units
    One day range limit applies
    Response contains commissioned production units for given day
    Mandatory parameters
        DocumentType
        BusinessType
        BiddingZone_Domain
        Implementation_DateAndOrTime
    Optional parameters
        PsrType
    """

    def __init__(
        self,
        biddingZone_Domain: Area = None,
        psrType: PsrType = None,
        implementation_DateAndOrTime: str = None,
    ):
        super(ProductionAndGenerationUnits, self).__init__(
            documentType=DocumentType.A95,
            businessType=BusinessType.B11,
            biddingZone_Domain=biddingZone_Domain,
            psrType=psrType,
            implementation_DateAndOrTime=implementation_DateAndOrTime,
        )
