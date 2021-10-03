from entsoe_client.Utils import ParameterEnum


class MarketAgreementType(str, ParameterEnum):
    A01 = ("Daily",)
    A02 = ("Weekly",)
    A03 = ("Monthly",)
    A04 = ("Yearly",)
    A05 = ("Total",)
    A06 = ("Long term",)
    A07 = ("Intraday",)
    A13 = "Hourly"
