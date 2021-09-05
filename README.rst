===============
ENTSO-E Client.
===============


| *ENTSO-E Client* enables straight-forward of access to *all* of the data at `ENTSO-E Transparency Platform <https://transparency.entsoe.eu/>`_.
* Query templates abstract the API specifics away through Enumerated types.
* Parse responses into Pandas DataFrames without loss of information.

| The separation of Queries, Client and Parser with their hierarchical abstractions keep the package extensible and maintainable.
 A pipeline from Query to DataFrame is trivial to build, preserving the ability to customize steps in between.

| The implementation relies primarily on the
 `Transparency Platform restful API - user guide <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_.
 The `Manual of Procedures (MoP) <https://www.entsoe.eu/data/transparency-platform/mop/>`_ documents provide
 further insight on the *business requirements specification*.
 Further information can be found in the
 `Electronic Data Interchange (EDI) Library <https://www.entsoe.eu/publications/electronic-data-interchange-edi-library/>`_.

| Related projects: ElectricityMap, EntsoePy, ...