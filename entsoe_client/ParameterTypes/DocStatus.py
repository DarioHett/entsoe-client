from entsoe_client.Utils import ParameterEnum


class DocStatus(str, ParameterEnum):
    A01 = ("Intermediate",)
    A02 = ("Final",)
    A05 = ("Active",)
    A09 = ("Cancelled",)
    A13 = ("Withdrawn",)
    X01 = ("Estimated",)
