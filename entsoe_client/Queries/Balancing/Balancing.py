from entsoe_client.ParameterTypes import *
from entsoe_client.Queries import Query


class Balancing(Query):
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
    ):
        """
        Appendix A: Complete parameter list
        A.1.Available parameters
        """
        super(Balancing, self).__init__(
            documentType=documentType,
            docStatus=docStatus,
            processType=processType,
            businessType=businessType,
            psrType=psrType,
            type_MarketAgreementType=type_MarketAgreementType,
            contract_MarketAgreementType=contract_MarketAgreementType,
            auctionType=auctionType,
            auctionCategory=auctionCategory,
            classificationSequence_AttributeInstanceComponent_Position=classificationSequence_AttributeInstanceComponent_Position,
            outBiddingZone_Domain=outBiddingZone_Domain,
            biddingZone_Domain=biddingZone_Domain,
            controlArea_Domain=controlArea_Domain,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            Acquiring_Domain=Acquiring_Domain,
            Connecting_Domain=Connecting_Domain,
            registeredResource=registeredResource,
            timeInterval=timeInterval,
            periodStart=periodStart,
            periodEnd=periodEnd,
            timeIntervalUpdate=timeIntervalUpdate,
            periodStartUpdate=periodStartUpdate,
            periodEndUpdate=periodEndUpdate,
            update_DateAndOrTime=update_DateAndOrTime,
            Area_Domain=Area_Domain,
            implementation_DateAndOrTime=implementation_DateAndOrTime,
            offset=offset,
        )


class CurrentBalancingState(Balancing):
    """
    4.6.1. Current Balancing State [GL EB 12.3.A]
        100 day range limit applies
        Mandatory Parameters
            DocumentType
            BusinessType
            Area_Domain
            TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        Area_Domain=None,  # Does not appear in documentation.
        periodStart=None,
        periodEnd=None,
    ):
        super(CurrentBalancingState, self).__init__(
            documentType=DocumentType.A86,
            businessType=BusinessType.B33,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class AggregatedBalancingEnergyBids(Balancing):
    """
    4.6.2. Aggregated Balancing Energy Bids [GL EB 12.3.E]
    One year range limit applies
    Mandatory Parameters
        DocumentType
        ProcessType
        Area_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd

    ProcessType can potentially vary (different reserves);
    ENTSOE Example uses aFRR (A51).
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A51,
        Area_Domain: Area = None,  # Does not appear in documentation.
        periodStart=None,
        periodEnd=None,
    ):
        super(AggregatedBalancingEnergyBids, self).__init__(
            documentType=DocumentType.A24,
            processType=processType,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class ProcuredBalancingCapacity(Balancing):
    """
    4.6.3.  Procured Balancing Capacity [GL EB 12.3.F]
        100 document limit applies
        Mandatory Parameters
            DocumentType
            ProcessType
            Area_Domain
            TimeInterval or combination of PeriodStart and PeriodEnd
        Optional Parameters
            Type_MarketAgreement.Type

    ProcessType can potentially vary (different reserves);
    ENTSOE Example uses aFRR (A51).
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A51,
        Area_Domain: Area = None,  # Does not appear in documentation.
        periodStart=None,
        periodEnd=None,
        type_MarketAgreementType: MarketAgreementType = None,
    ):
        super(ProcuredBalancingCapacity, self).__init__(
            documentType=DocumentType.A15,
            processType=processType,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            type_MarketAgreementType=type_MarketAgreementType,
        )


class UseOfAllocatedCrossZonalBalancingCapacity(Balancing):
    """
    4.6.4. Use of Allocated Cross-Zonal Balancing Capacity [GL EB 12.3.H&I]
        Mandatory parameters
            DocumentType
            ProcessType
            Acquiring_Domain
            Connecting_Domain
            TimeInterval or combination of PeriodStart and PeriodEnd
        Optional parameters
            Type_MarketAgreement.Type

    ProcessType can potentially vary (different reserves);
    ENTSOE Example uses replacement reserve (A46).
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A46,
        periodStart=None,
        periodEnd=None,
        Acquiring_Domain: Area = None,
        Connecting_Domain: Area = None,
        type_MarketAgreementType: MarketAgreementType = None,
    ):
        super(UseOfAllocatedCrossZonalBalancingCapacity, self).__init__(
            documentType=DocumentType.A38,
            processType=processType,
            Acquiring_Domain=Acquiring_Domain,
            Connecting_Domain=Connecting_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            type_MarketAgreementType=type_MarketAgreementType,
        )


class AmountOfBalancingReservesUnderContract(Balancing):
    """
    4.6.5. Amount of Balancing Reserves Under Contract [17.1.B]
        Minimum time interval in query response ranges from part of day to year, depending on selected Type_MarketAgreement.Type
        Mandatory parameters
            DocumentType
            Type_MarketAgreement.Type
            ControlArea_Domain
            TimeInterval or combination of PeriodStart and PeriodEnd
        Optional parameters
            BusinessType
            PsrType
            offset (allows downloading more than 100 documents.
            The offset ∈ [0,4800] so that paging is restricted to query for 4900 documents max.,
            offset=n returns files in sequence between n+1 and n+100)
    """

    def __init__(
        self,
        type_MarketAgreementType: MarketAgreementType = None,
        controlArea_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType.A95,
        psrType: PsrType = None,
        offset: int = None,
    ):
        super(AmountOfBalancingReservesUnderContract, self).__init__(
            documentType=DocumentType.A81,
            type_MarketAgreementType=type_MarketAgreementType,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            psrType=psrType,
            offset=offset,
        )


class PricesOfProcuredBalancingReserves(Balancing):
    """
    4.6.6. Prices of Procured Balancing Reserves [17.1.C]
    Minimum time interval in query response ranges from part of day to year, depending on selected Type_MarketAgreement.Type
    Mandatory parameters
        DocumentType
        Type_MarketAgreement.Type
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        PsrType
        offset (allows downloading more than 100 documents.
                The offset ∈ [0,4800] so that paging is restricted to query for 4900 documents max.,
                offset=n returns files in sequence between n+1 and n+100)
    """

    def __init__(
        self,
        type_MarketAgreementType: MarketAgreementType = MarketAgreementType("Daily"),
        controlArea_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType("Frequency containment reserve"),
        psrType: PsrType = None,
        offset: int = None,
    ):
        super(PricesOfProcuredBalancingReserves, self).__init__(
            documentType=DocumentType.A89,
            type_MarketAgreementType=type_MarketAgreementType,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            psrType=psrType,
            offset=offset,
        )


class AcceptedAggregatedOffers(Balancing):
    """
    4.6.7. Accepted Aggregated Offers [17.1.D]
    One year range limit applies
    Minimum time interval in query response is one BTU period
    Mandatory parameters
        DocumentType
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        PsrType
    """

    def __init__(
        self,
        controlArea_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType("Frequency containment reserve"),
        psrType: PsrType = None,
    ):
        super(AcceptedAggregatedOffers, self).__init__(
            documentType=DocumentType.A82,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            psrType=psrType,
        )


class ActivatedBalancingEnergy(Balancing):
    """
    4.6.8. Activated Balancing Energy [17.1.E]
    One year range limit applies
    Minimum time interval in query response is one BTU period
    Mandatory parameters
        DocumentType
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        PsrType

    BusinessType can potentially vary (different reserves);
    ENTSOE Example uses FCR.
    """

    def __init__(
        self,
        controlArea_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType("Frequency containment reserve"),
        psrType: PsrType = None,
    ):
        super(ActivatedBalancingEnergy, self).__init__(
            documentType=DocumentType.A83,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            psrType=psrType,
        )


class PricesOfActivatedBalancingEnergy(Balancing):
    """
    4.6.9. Prices of Activated Balancing Energy [17.1.F]
    One year range limit applies
    Minimum time interval in query response is one BTU period
    Mandatory parameters
        DocumentType
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        PsrType

    BusinessType can potentially vary (different reserves);
    ENTSOE Example uses aFRR (A96).
    """

    def __init__(
        self,
        controlArea_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType("Frequency containment reserve"),
        psrType: PsrType = None,
    ):
        super(PricesOfActivatedBalancingEnergy, self).__init__(
            documentType=DocumentType.A84,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            psrType=psrType,
        )


class ImbalancePrices(Balancing):
    """
    4.6.10. Imbalance Prices [17.1.G]
    One year range limit applies
    Minimum time interval in query response is one BTU period
    Mandatory parameters
        DocumentType
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        PsrType
    """

    def __init__(
        self,
        controlArea_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        psrType: PsrType = None,
    ):
        super(ImbalancePrices, self).__init__(
            documentType=DocumentType.A85,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            psrType=psrType,
        )


class TotalImbalanceVolumes(Balancing):
    """
    4.6.11. Total Imbalance Volumes [17.1.H]
    One year range limit applies
    Minimum time interval in query response is one BTU period
    Mandatory parameters
        DocumentType
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self, controlArea_Domain: Area = None, periodStart=None, periodEnd=None
    ):
        super(TotalImbalanceVolumes, self).__init__(
            documentType=DocumentType.A86,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class FinancialExpensesAndIncomeForBalancing(Balancing):
    """
    4.6.12. Financial Expenses and Income for Balancing [17.1.I]
    One year range limit applies
    Minimum time interval in query response is one month
    Mandatory parameters
        DocumentType
        ControlArea_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self, controlArea_Domain: Area = None, periodStart=None, periodEnd=None
    ):
        super(FinancialExpensesAndIncomeForBalancing, self).__init__(
            documentType=DocumentType.A87,
            controlArea_Domain=controlArea_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class CrossborderBalancing(Balancing):
    """
    4.6.13. Cross-border Balancing [17.1.J]
    One year range limit applies
    Minimum time interval in query response is one BTU period
    Mandatory parameters
        DocumentType
        Acquiring_Domain
        Connecting_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    In the query response, the attribute secondaryQuantity contains the Aggregated offers,
    quantity contains the activated offers and prices are available in the minimum_Price.amount and
    maximum_Price.amount attributes.
    """

    def __init__(
        self,
        Acquiring_Domain: Area = None,
        Connecting_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
    ):
        super(CrossborderBalancing, self).__init__(
            documentType=DocumentType.A88,
            Acquiring_Domain=Acquiring_Domain,
            Connecting_Domain=Connecting_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class FCRTotalCapacity(Balancing):
    """
    4.6.14. FCR Total capacity [SO GL 187.2]
    One year range limit applies
    Mandatory parameters
        DocumentType
        BusinessType
        Area_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(
        self,
        businessType: BusinessType = BusinessType.A25,
        Area_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
    ):
        super(FCRTotalCapacity, self).__init__(
            documentType=DocumentType.A26,
            businessType=businessType,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class SharesOfFCRCapacity_ShareOfCapacity(Balancing):
    """
    4.6.15. Shares of FCR capacity - share of capacity [SO GL 187.2]
    One year range limit applies
    Mandatory parameters
        DocumentType
        BusinessType
        Area_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(self, Area_Domain: Area = None, periodStart=None, periodEnd=None):
        super(SharesOfFCRCapacity_ShareOfCapacity, self).__init__(
            documentType=DocumentType.A26,
            businessType=BusinessType.C23,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class SharesOfFCRCapacity_ContractedReserveCapacity(Balancing):
    """
    4.6.16. Shares of FCR capacity - contracted reserve capacity [SO GL 187.2]
    One year range limit applies
    Mandatory parameters
        DocumentType
        BusinessType
        Area_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(self, Area_Domain: Area = None, periodStart=None, periodEnd=None):
        super(SharesOfFCRCapacity_ContractedReserveCapacity, self).__init__(
            documentType=DocumentType.A26,
            businessType=BusinessType.B95,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class FRRActualCapacity(Balancing):
    """
    4.6.17. FRR Actual Capacity [SO GL 188.4]
    Mandatory parameters
        DocumentType
        ProcessType
        BusinessType
        Area_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(self, Area_Domain: Area = None, periodStart=None, periodEnd=None):
        super(FRRActualCapacity, self).__init__(
            documentType=DocumentType.A26,
            processType=ProcessType.A56,
            businessType=BusinessType.C24,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class RRActualCapacity(Balancing):
    """
    4.6.18. RR Actual Capacity [SO GL 189.3]
    Mandatory parameters
        DocumentType
        ProcessType
        BusinessType
        Area_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    """

    def __init__(self, Area_Domain: Area = None, periodStart=None, periodEnd=None):
        super(RRActualCapacity, self).__init__(
            documentType=DocumentType.A26,
            processType=ProcessType.A46,
            businessType=BusinessType.C24,
            Area_Domain=Area_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )


class SharingOfRRAndFRR(Balancing):
    """
    4.6.19. Sharing of RR and FRR [SO GL 190.1]
    One year range limit applies
    Mandatory parameters
        DocumentType
        BusinessType
        ProcessType
        Acquiring_Domain
        Connecting_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd

    ProcessType can potentially vary (different reserves);
    ENTSOE Example uses FRR (A56).
    """

    def __init__(
        self,
        processType: ProcessType = ProcessType.A56,
        Acquiring_Domain: Area = None,
        Connecting_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
    ):
        super(SharingOfRRAndFRR, self).__init__(
            documentType=DocumentType.A26,
            businessType=BusinessType.C22,
            processType=processType,
            Acquiring_Domain=Acquiring_Domain,
            Connecting_Domain=Connecting_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
        )
