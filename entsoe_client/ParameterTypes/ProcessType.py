from entsoe_client.Utils import ParameterEnum


class ProcessType(str, ParameterEnum):
    A01 = ("Day ahead",)
    A02 = ("Intra day incremental",)
    A16 = ("Realised",)
    A18 = ("Intraday total",)
    A31 = ("Week ahead",)
    A32 = ("Month ahead",)
    A33 = ("Year ahead",)
    A39 = ("Synchronisation process",)
    A40 = ("Intraday process",)
    A46 = ("Replacement reserve",)
    A47 = ("Manual frequency restoration reserve",)
    A51 = ("Automatic frequency restoration reserve",)
    A52 = ("Frequency containment reserve",)
    A56 = "Frequency restoration reserve"
