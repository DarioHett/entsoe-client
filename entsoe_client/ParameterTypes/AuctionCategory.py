from entsoe_client.Utils import ParameterEnum


class AuctionCategory(str, ParameterEnum):
    A01 = ("Base",)
    A02 = ("Peak",)
    A03 = ("Off Peak",)
    A04 = "Hourly"
