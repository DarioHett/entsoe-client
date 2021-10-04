===============
ENTSO-E Client
===============

Formulate readable queries and handle data in Pandas,
including an exhaustive set of pre-defined queries.

.. code-block:: python

    >>> import requests
    >>> from lxml import objectify
    >>> from lxml.etree import dump
    >>> url = 'https://transparency.entsoe.eu/api?' \
    ...       'documentType=A81&businessType=A95&psrType=A04&type_MarketAgreement.Type=A01&controlArea_Domain=10YNL----------L' \
    ...       f'&periodStart=202101010000&periodEnd=202104010000&securityToken={api_key}'
    >>> response = requests.Session().get(url=url)
    >>> element = objectify.fromstring(response.content)
    >>> dump(element)
    <Balancing_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:3:0">
      <mRID>051b91beed574b48b4548214e9001afc</mRID>
      <revisionNumber>1</revisionNumber>
      <type>A81</type>
      <process.processType>A34</process.processType>
      <sender_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</sender_MarketParticipant.mRID>
      <sender_MarketParticipant.marketRole.type>A32</sender_MarketParticipant.marketRole.type>
      <receiver_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</receiver_MarketParticipant.mRID>
      <receiver_MarketParticipant.marketRole.type>A33</receiver_MarketParticipant.marketRole.type>
      <createdDateTime>2021-10-04T18:12:43Z</createdDateTime>
      <controlArea_Domain.mRID codingScheme="A01">10YNL----------L</controlArea_Domain.mRID>
      <period.timeInterval>
        <start>2020-12-31T23:00Z</start>
        <end>2021-03-31T22:00Z</end>
      </period.timeInterval>
      <TimeSeries>
        <mRID>1</mRID>
        <businessType>A95</businessType>
        <type_MarketAgreement.type>A01</type_MarketAgreement.type>
        <mktPSRType.psrType>A04</mktPSRType.psrType>
        <flowDirection.direction>A03</flowDirection.direction>
        <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
        <curveType>A01</curveType>
        <Period>
          <timeInterval>
            <start>2020-12-31T23:00Z</start>
            <end>2021-01-01T23:00Z</end>
          </timeInterval>
          <resolution>PT60M</resolution>
          <Point>
            <position>1</position>
            <quantity>44</quantity>
          </Point>
          <Point>
            <position>2</position>
            <quantity>44</quantity>
    [...]

becomes

.. code-block:: python

    >>> import entsoe_client as ec
    >>> from entsoe_client.ParameterTypes import *
    >>> client = ec.Client(api_key)
    >>> parser = ec.Parser
    >>> query = ec.Query(
    ...     documentType=DocumentType("Contracted reserves"),
    ...     psrType=PsrType("Generation"),
    ...     businessType=BusinessType("Frequency containment reserve"),
    ...     controlArea_Domain=Area("NL"),
    ...     type_MarketAgreementType=MarketAgreementType("Daily"),
    ...     periodStart="2021-01-01T00:00",
    ...     periodEnd="2021-04-01T00:00"
    ... )
    >>> response = client(query)
    >>> df = parser.parse(response)
    >>> df.iloc[:,:3].head()
                              position quantity Period.timeInterval.start...
    2020-12-31 23:00:00+00:00        1       44         2020-12-31T23:00Z
    2021-01-01 00:00:00+00:00        2       44         2020-12-31T23:00Z
    2021-01-01 01:00:00+00:00        3       44         2020-12-31T23:00Z
    2021-01-01 02:00:00+00:00        4       44         2020-12-31T23:00Z
    2021-01-01 03:00:00+00:00        5       44         2020-12-31T23:00Z
    ...


predefined queries are subset of the generic Query class, covering all examples of the `ENTSO-E API guide <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_.

.. code-block:: python

    >>> predefined_query = ec.Queries.Balancing.AmountOfBalancingReservesUnderContract(
    ...     controlArea_Domain=Area("NL"),
    ...     type_MarketAgreementType=MarketAgreementType("Daily"),
    ...     psrType=PsrType("Generation"),
    ...     periodStart="2021-01-01T00:00",
    ...     periodEnd="2021-04-01T00:00"
    ... )
    ...
    >>> predefined_query() == query()
    True

-----

| *ENTSO-E Client* enables straight-forward access to *all* of the data at `ENTSO-E Transparency Platform <https://transparency.entsoe.eu/>`_.

* Query templates abstract the API specifics through Enumerated types.

* Parse responses into Pandas DataFrames without loss of *any* information.

| The separation of Queries, Client and Parser with their hierarchical abstractions keep the package extensible and maintainable. A pipeline from Query to DataFrame is trivial, preserving the ability to customize steps in between.

| The implementation relies primarily on the
 `Transparency Platform restful API - user guide <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_.
 The `Manual of Procedures (MoP) <https://www.entsoe.eu/data/transparency-platform/mop/>`_ documents provide
 further insight on the *business requirements specification*.
 Further information can be found in the
 `Electronic Data Interchange (EDI) Library <https://www.entsoe.eu/publications/electronic-data-interchange-edi-library/>`_.

-----

Main contributions

* Exhaustive List of ParameterTypes.
    These allow mapping between natural language and the codes required
    for GET requests, e.g. :code:`DocumentType.A85 == DocumentType("Imbalance price")`.
    This feature allows keeping track of queries without jumping between documents or adding comments.

* Exhaustive List of Pre-defined Queries from ENTSO-E API Guide.
    `ENTSO-E API Guide <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_
    is a minial set for any API connector to implement and reflects all dashboards on
    ENTSO-E Transparency Platform.

* Parsers
    Response `Documents` come in XML schema which can be parsed into pandas DataFrames.

    Implemented: GL_MarketDocuments, TransmissionNetwork_MarketDocuments,
    Publication_MarketDocuments and Balancing_MarketDocuments.

    Missing: Outages, Congestion Management and System Operations.

Nevertheless, ENTSO-E Client seeks to be minimal to go from Query to DataFrame and requires domain-
knowledge on how to formulate queries and interpret various columns of a parsed response.

-----

ENTSO-E relies on many codes (`Type`) to map to desired queries.
Types are encoded in Enum classes with a .help() function to list the all.
They can be addressed through Type[code] or Type(string), making interaction
easy. HTTP requests and responses usually require the `code`, whereas we
want to formulate the query as a human-readable `string`.

::

    from entsoe_client import Queries
    from entsoe_client.ParameterTypes import *

    Queries.Transmission.CapacityAllocatedOutsideEU(
            out_Domain=Area('SK'),
            in_Domain=Area('UA_BEI'),
            marketAgreementType=MarketAgreementType('Daily'), # Original code: A01
            auctionType=AuctionType('Explicit'), # Original code: A02
            auctionCategory=AuctionCategory('Hourly'), # Original code: A04
            classificationSequence_AttributeInstanceComponent_Position=1,
            periodStart=201601012300,
            periodEnd=201601022300)

::

    >>> ParameterTypes.DocumentType['A25'] == ParameterTypes.DocumentType('Allocation result document')
    True
    >>> ec.ParameterTypes.DocumentType.help()
    --- DocumentType ---
    API_PARAMETER: DESCRIPTION
    [...]
    A25: Allocation result document
    A71: Generation forecast
    A72: Reservoir filling information
    A73: Actual generation
    A85: Imbalance prices
    A86: Imbalance volume
    [...]
    API_PARAMETER: DESCRIPTION
    --- DocumentType ---
    >>> ec.ParameterTypes.BusinessType.help()
    --- BusinessType ---
    API_PARAMETER: DESCRIPTION
    [...]
    A25: General Capacity Information
    A29: Already allocated capacity(AAC)
    A97: Manual frequency restoration reserve
    B08: Total nominated capacity
    C22: Shared Balancing Reserve Capacity
    C24: Actual reserve capacity
    [...]
    API_PARAMETER: DESCRIPTION
    --- BusinessType ---

::

    #shortened from sample_plot.py
    import entsoe_client as ec
    from settings import api_key

    # Instantiate Client, Parser and Query.
    client = ec.Client(api_key)
    parser = ec.Parser()
    query = ec.Queries.Generation.AggregatedGenerationPerType(
        in_Domain=ec.ParameterTypes.Area('DE_LU'),
        periodStart=202109050200,
        periodEnd=202109070200)

    # Extract data.
    response = client(query)
    df = parser(response)
    [...]

    # Transform data.
    production = df[~consumption_mask][['quantity', 'TimeSeries.MktPSRType.psrType']]
    ## PsrType, e.g. `B01` := `Biomass`.
    production['GenerationType'] = production['TimeSeries.MktPSRType.psrType']. \
        apply(lambda x: ParameterTypes.PsrType[x].value) # Map ENTSO-E PsrTypes into human-readable string.
    production_by_type = pd.pivot_table(production,
                                        index=production.index,
                                        columns='GenerationType',
                                        values='quantity')
    [...]
    # Plot.
    production_by_type.plot.bar(title="Production by Generation Type in DE-LU",
                                xlabel="UTC",
                                ylabel='MWh',
                                ax=ax,
                                **plot_params)
    [...]


.. image:: ./sample_plot.png
