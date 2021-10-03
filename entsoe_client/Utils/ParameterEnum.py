from enum import Enum, unique


@unique
class ParameterEnum(Enum):
    @classmethod
    def dict(cls):
        return dict(map(lambda c: (c.name, c.value), cls))

    @classmethod
    def help(cls):
        prefix = ["--- " + cls.__name__ + " ---"]
        schema = ["API_PARAMETER: DESCRIPTION"]
        key_value_list = [f"{k}: {v}" for (k, v) in cls.dict().items()]
        suffix = ["--- " + cls.__name__ + " ---"]
        help_string = "\n".join(prefix + schema + key_value_list + schema + suffix)
        print(help_string)
