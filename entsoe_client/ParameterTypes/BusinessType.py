from entsoe_client.Utils import ParameterEnum


class BusinessType(str, ParameterEnum):
    A25 = ("General Capacity Information",)
    A29 = ("Already allocated capacity(AAC)",)
    A43 = ("Requested capacity(without price)",)
    A46 = ("System Operator redispatching",)
    A53 = ("Planned maintenance ",)
    A54 = ("Unplanned outage A85 Internal redispatch",)
    A95 = ("Frequency containment reserve",)
    A96 = ("Automatic frequency restoration reserve",)
    A97 = ("Manual frequency restoration reserve",)
    A98 = ("Replacement reserve",)
    B01 = ("Interconnector network evolution",)
    B02 = ("Interconnector network dismantling",)
    B03 = ("Counter trade",)
    B04 = ("Congestion costs",)
    B05 = ("Capacity allocated(including price)",)
    B07 = ("Auction revenue",)
    B08 = ("Total nominated capacity",)
    B09 = ("Net position",)
    B10 = ("Congestion income",)
    B11 = ("Production unit",)
    B33 = ("Area Control Error",)
    B95 = ("Procured capacity",)
    C22 = ("Shared Balancing Reserve Capacity",)
    C23 = ("Share of reserve capacity",)
    C24 = "Actual reserve capacity"
