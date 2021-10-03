from entsoe_client.ParameterTypes import *
from entsoe_client.Queries import Query


class Outages(Query):
    """
    4.7. Outages
    Response for articles 10.1 and 15.1 is ZIP folder with one document inside it for each outage.
    Withdrawn outages are not returned unless "docStatus=A13" parameter is added to the requested query.
    Older versions of an outage is returned only when mRID parameter is used.
    Additional information - To extract outages of bidding zone  DE-AT-LU area,
    it is  recommended to send queries per control area i.e.
    CTA|DE(50Hertz), CTA|DE(Amprion), CTA|DE(TeneTGer),CTA|DE(TransnetBW),CTA|AT,CTA|LU but not per bidding zone.
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
        super(Outages, self).__init__(
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
            mRID=mRID,
        )


class UnavailabilityOfConsumptionUnits(Outages):
    """
    4.7.1. Unavailability of Consumption Units [7.1A&B]
    One year range limit applies
    Minimum time interval in query response is one MTU period
    Mandatory parameters
        DocumentType
        BiddingZone_Domain
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
    """

    def __init__(
        self,
        biddingZone_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = None,
    ):
        super(UnavailabilityOfConsumptionUnits, self).__init__(
            documentType=DocumentType.A76,
            biddingZone_Domain=biddingZone_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
        )


class UnavailabilityOfTransmissionInfrastructure(Outages):
    """
    4.7.2. Unavailability of Transmission Infrastructure [10.1.A&B]
    One year range limit applies
        It applies to PeriodStart and PeriodEnd if PeriodStartUpdate and PeriodEndUpdate parameters are not mentioned.
        It applies only to PeriodStartUpdate and PeriodEndUpdate if mentioned.
    200 documents limit applies
    Minimum time interval in query response depends on duration of matching outages
    Mandatory parameters
        DocumentType
        In_Domain (Optional if mRID is present)
        Out_Domain (Optional if mRID is present)
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        DocStatus
        TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
        mRID
        offset (allows downloading more than 200 documents.
                The offset ∈ [0,4800] so that pagging is restricted to query for 5000 documents max.,
                offset=n returns files in sequence between n+1 and n+200)

    TODO: Missing Parameter: TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
    """

    def __init__(
        self,
        in_Domain: Area = None,
        out_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType.A53,
        docStatus: DocStatus = None,
        mRID: int = None,
        offset: int = None,
    ):
        super(UnavailabilityOfTransmissionInfrastructure, self).__init__(
            documentType=DocumentType.A78,
            in_Domain=in_Domain,
            out_Domain=out_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            docStatus=docStatus,
            mRID=mRID,
            offset=offset,
        )


class UnavailabilityOfOffshoreGridInfrastructure(Outages):
    """
    4.7.3. Unavailability of Offshore Grid Infrastructure [10.1.C]
    One year range limit applies
        It applies to PeriodStart and PeriodEnd if PeriodStartUpdate and PeriodEndUpdate parameters are not mentioned.
        It applies only to PeriodStartUpdate and PeriodEndUpdate if mentioned.
    200 documents limit applies
    Minimum time interval in query response depends on duration of matching outages
    Mandatory parameters
        DocumentType
        BiddingZone_Domain (Optional if mRID is present)
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        DocStatus
        TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
        mRID
        offset (allows downloading more than 200 documents.
                The offset ∈ [0,4800] so that pagging is restricted to query for 5000 documents max.,
                offset=n returns files in sequence between n+1 and n+200)

    TODO: Missing Parameter: TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
    """

    def __init__(
        self,
        biddingZone_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        docStatus: DocStatus = None,
        mRID: int = None,
        offset: int = None,
    ):
        super(UnavailabilityOfOffshoreGridInfrastructure, self).__init__(
            documentType=DocumentType.A79,
            biddingZone_Domain=biddingZone_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            docStatus=docStatus,
            mRID=mRID,
            offset=offset,
        )


class UnavailabilityOfGenerationUnits(Outages):
    """
    4.7.4. Unavailability of Generation Units [15.1.A&B]
    One year range limit applies
        It applies to PeriodStart and PeriodEnd if PeriodStartUpdate and PeriodEndUpdate parameters are not mentioned.
        It applies only to PeriodStartUpdate and PeriodEndUpdate if mentioned.
    200 documents limit applies
    Minimum time interval in query response depends on duration of matching outages
    Mandatory parameters
        DocumentType
        BiddingZone_Domain (Optional if mRID is present)
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        DocStatus
        TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
        RegisteredResource
        mRID
        offset (allows downloading more than 200 documents.
                The offset ∈ [0,4800] so that pagging is restricted to query for 5000 documents max.,
                offset=n returns files in sequence between n+1 and n+200)

    TODO: Missing Parameter: TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
    """

    def __init__(
        self,
        biddingZone_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType.A53,
        docStatus: DocStatus = None,
        registeredResource=None,
        mRID: int = None,
        offset: int = None,
    ):
        super(UnavailabilityOfGenerationUnits, self).__init__(
            documentType=DocumentType.A80,
            biddingZone_Domain=biddingZone_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            docStatus=docStatus,
            registeredResource=registeredResource,
            mRID=mRID,
            offset=offset,
        )


class UnavailabilityOfProductionUnits(Outages):
    """
    4.7.5. Unavailability of Production Units [15.1.C&D]
    One year range limit applies
        It applies to PeriodStart and PeriodEnd if PeriodStartUpdate and PeriodEndUpdate parameters are not mentioned.
        It applies only to PeriodStartUpdate and PeriodEndUpdate if mentioned.
    200 documents limit applies
    Minimum time interval in query response depends on duration of matching outages
    Mandatory parameters
        DocumentType
        BiddingZone_Domain (Optional if mRID is present)
        TimeInterval or combination of PeriodStart and PeriodEnd
    Optional parameters
        BusinessType
        DocStatus
        TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
        RegisteredResource
        mRID
        offset (allows downloading more than 200 documents.
                The offset ∈ [0,4800] so that pagging is restricted to query for 5000 documents max.,
                offset=n returns files in sequence between n+1 and n+200)

    TODO: Missing Parameter: TimeIntervalUpdate or combination of PeriodStartUpdate and PeriodEndUpdate
    """

    def __init__(
        self,
        biddingZone_Domain: Area = None,
        periodStart=None,
        periodEnd=None,
        businessType: BusinessType = BusinessType.A53,
        docStatus: DocStatus = None,
        registeredResource=None,
        mRID: int = None,
        offset: int = None,
    ):
        super(UnavailabilityOfProductionUnits, self).__init__(
            documentType=DocumentType.A77,
            biddingZone_Domain=biddingZone_Domain,
            periodStart=periodStart,
            periodEnd=periodEnd,
            businessType=businessType,
            docStatus=docStatus,
            registeredResource=registeredResource,
            mRID=mRID,
            offset=offset,
        )
