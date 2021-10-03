from entsoe_client.Utils import ParameterEnum


class AuctionType(str, ParameterEnum):
    A01 = ("Implicit",)
    A02 = ("Explicit",)
