from entsoe_client.Utils import ParameterEnum


class Area(ParameterEnum):
    """
    ENUM containing 3 things about an Area: CODE, Meaning, Timezone
    """
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, meaning: str, tz: str):
        self._meaning = meaning
        self._tz = tz

    def __str__(self):
        return self.value

    @property
    def meaning(self):
        return self._meaning

    @property
    def tz(self):
        return self._tz

    @property
    def code(self):
        return self.value

    # List taken directly from the API Docs
    DE_50HZ =       '10YDE-VE-------2', '50Hertz CA, DE(50HzT) BZA',                    'Europe/Berlin',
    AL =            '10YAL-KESH-----5', 'Albania, OST BZ / CA / MBA',                   'Europe/Tirane',
    DE_AMPRION =    '10YDE-RWENET---I', 'Amprion CA',                                   'Europe/Berlin',
    AT =            '10YAT-APG------L', 'Austria, APG BZ / CA / MBA',                   'Europe/Vienna',
    BY =            '10Y1001A1001A51S', 'Belarus BZ / CA / MBA',                        'Europe/Minsk',
    BE =            '10YBE----------2', 'Belgium, Elia BZ / CA / MBA',                  'Europe/Brussels',
    BA =            '10YBA-JPCC-----D', 'Bosnia Herzegovina, NOS BiH BZ / CA / MBA',    'Europe/Sarajevo',
    BG =            '10YCA-BULGARIA-R', 'Bulgaria, ESO BZ / CA / MBA',                  'Europe/Sofia',
    CZ_DE_SK =      '10YDOM-CZ-DE-SKK', 'BZ CZ+DE+SK BZ / BZA',                         'Europe/Prague',
    HR =            '10YHR-HEP------M', 'Croatia, HOPS BZ / CA / MBA',                  'Europe/Zagreb',
    CWE =           '10YDOM-REGION-1V', 'CWE Region',                                   'Europe/Brussels',
    CY =            '10YCY-1001A0003J', 'Cyprus, Cyprus TSO BZ / CA / MBA',             'Asia/Nicosia',
    CZ =            '10YCZ-CEPS-----N', 'Czech Republic, CEPS BZ / CA/ MBA',            'Europe/Prague',
    DE_AT_LU =      '10Y1001A1001A63L', 'DE-AT-LU BZ',                                  'Europe/Berlin',
    DE_LU =         '10Y1001A1001A82H', 'DE-LU BZ / MBA',                               'Europe/Berlin',
    DK =            '10Y1001A1001A65H', 'Denmark',                                      'Europe/Copenhagen',
    DK_1 =          '10YDK-1--------W', 'DK1 BZ / MBA',                                 'Europe/Copenhagen',
    DK_2 =          '10YDK-2--------M', 'DK2 BZ / MBA',                                 'Europe/Copenhagen',
    DK_CA =         '10Y1001A1001A796', 'Denmark, Energinet CA',                        'Europe/Copenhagen',
    EE =            '10Y1001A1001A39I', 'Estonia, Elering BZ / CA / MBA',               'Europe/Tallinn',
    FI =            '10YFI-1--------U', 'Finland, Fingrid BZ / CA / MBA',               'Europe/Helsinki',
    MK =            '10YMK-MEPSO----8', 'Former Yugoslav Republic of Macedonia, MEPSO BZ / CA / MBA', 'Europe/Skopje',
    FR =            '10YFR-RTE------C', 'France, RTE BZ / CA / MBA',                    'Europe/Paris',
    DE =            '10Y1001A1001A83F', 'Germany',                                      'Europe/Berlin'
    GR =            '10YGR-HTSO-----Y', 'Greece, IPTO BZ / CA/ MBA',                    'Europe/Athens',
    HU =            '10YHU-MAVIR----U', 'Hungary, MAVIR CA / BZ / MBA',                 'Europe/Budapest',
    IS =            'IS',               'Iceland',                                      'Atlantic/Reykjavik',
    IE_SEM =        '10Y1001A1001A59C', 'Ireland (SEM) BZ / MBA',                       'Europe/Dublin',
    IE =            '10YIE-1001A00010', 'Ireland, EirGrid CA',                          'Europe/Dublin',
    IT =            '10YIT-GRTN-----B', 'Italy, IT CA / MBA',                           'Europe/Rome',
    IT_SACO_AC =    '10Y1001A1001A885', 'Italy_Saco_AC',                                'Europe/Rome',
    IT_CALA =   '10Y1001C--00096J', 'IT-Calabria BZ',                                'Europe/Rome',
    IT_SACO_DC =    '10Y1001A1001A893', 'Italy_Saco_DC',                                'Europe/Rome',
    IT_BRNN =       '10Y1001A1001A699', 'IT-Brindisi BZ',                               'Europe/Rome',
    IT_CNOR =       '10Y1001A1001A70O', 'IT-Centre-North BZ',                           'Europe/Rome',
    IT_CSUD =       '10Y1001A1001A71M', 'IT-Centre-South BZ',                           'Europe/Rome',
    IT_FOGN =       '10Y1001A1001A72K', 'IT-Foggia BZ',                                 'Europe/Rome',
    IT_GR =         '10Y1001A1001A66F', 'IT-GR BZ',                                     'Europe/Rome',
    IT_MACRO_NORTH = '10Y1001A1001A84D', 'IT-MACROZONE NORTH MBA',                      'Europe/Rome',
    IT_MACRO_SOUTH = '10Y1001A1001A85B', 'IT-MACROZONE SOUTH MBA',                      'Europe/Rome',
    IT_MALTA =      '10Y1001A1001A877', 'IT-Malta BZ',                                  'Europe/Rome',
    IT_NORD =       '10Y1001A1001A73I', 'IT-North BZ',                                  'Europe/Rome',
    IT_NORD_AT =    '10Y1001A1001A80L', 'IT-North-AT BZ',                               'Europe/Rome',
    IT_NORD_CH =    '10Y1001A1001A68B', 'IT-North-CH BZ',                               'Europe/Rome',
    IT_NORD_FR =    '10Y1001A1001A81J', 'IT-North-FR BZ',                               'Europe/Rome',
    IT_NORD_SI =    '10Y1001A1001A67D', 'IT-North-SI BZ',                               'Europe/Rome',
    IT_PRGP =       '10Y1001A1001A76C', 'IT-Priolo BZ',                                 'Europe/Rome',
    IT_ROSN =       '10Y1001A1001A77A', 'IT-Rossano BZ',                                'Europe/Rome',
    IT_SARD =       '10Y1001A1001A74G', 'IT-Sardinia BZ',                               'Europe/Rome',
    IT_SICI =       '10Y1001A1001A75E', 'IT-Sicily BZ',                                 'Europe/Rome',
    IT_SUD =        '10Y1001A1001A788', 'IT-South BZ',                                  'Europe/Rome',
    RU_KGD =        '10Y1001A1001A50U', 'Kaliningrad BZ / CA / MBA',                    'Europe/Kaliningrad',
    LV =            '10YLV-1001A00074', 'Latvia, AST BZ / CA / MBA',                    'Europe/Riga',
    LT =            '10YLT-1001A0008Q', 'Lithuania, Litgrid BZ / CA / MBA',             'Europe/Vilnius',
    LU =            '10YLU-CEGEDEL-NQ', 'Luxembourg, CREOS CA',                         'Europe/Luxembourg',
    MT =            '10Y1001A1001A93C', 'Malta, Malta BZ / CA / MBA',                   'Europe/Malta',
    ME =            '10YCS-CG-TSO---S', 'Montenegro, CGES BZ / CA / MBA',               'Europe/Podgorica',
    GB =            '10YGB----------A', 'National Grid BZ / CA/ MBA',                   'Europe/London',
    NL =            '10YNL----------L', 'Netherlands, TenneT NL BZ / CA/ MBA',          'Europe/Amsterdam',
    NO_1 =          '10YNO-1--------2', 'NO1 BZ / MBA',                                 'Europe/Oslo',
    NO_2 =          '10YNO-2--------T', 'NO2 BZ / MBA',                                 'Europe/Oslo',
    NO_3 =          '10YNO-3--------J', 'NO3 BZ / MBA',                                 'Europe/Oslo',
    NO_4 =          '10YNO-4--------9', 'NO4 BZ / MBA',                                 'Europe/Oslo',
    NO_5 =          '10Y1001A1001A48H', 'NO5 BZ / MBA',                                 'Europe/Oslo',
    NO =            '10YNO-0--------C', 'Norway, Norway MBA, Stattnet CA',              'Europe/Oslo',
    PL_CZ =         '10YDOM-1001A082L', 'PL-CZ BZA / CA',                               'Europe/Warsaw',
    CZ_SK =         '10YDOM-1001A083J', 'CZ_SK BZA / CA',                               'Europe/Warsaw',
    PL =            '10YPL-AREA-----S', 'Poland, PSE SA BZ / BZA / CA / MBA',           'Europe/Warsaw',
    PT =            '10YPT-REN------W', 'Portugal, REN BZ / CA / MBA',                  'Europe/Lisbon',
    MD =            '10Y1001A1001A990', 'Republic of Moldova, Moldelectica BZ/CA/MBA',  'Europe/Chisinau',
    RO =            '10YRO-TEL------P', 'Romania, Transelectrica BZ / CA/ MBA',         'Europe/Bucharest',
    RU =            '10Y1001A1001A49F', 'Russia BZ / CA / MBA',                         'Europe/Moscow',
    SE_1 =          '10Y1001A1001A44P', 'SE1 BZ / MBA',                                 'Europe/Stockholm',
    SE_2 =          '10Y1001A1001A45N', 'SE2 BZ / MBA',                                 'Europe/Stockholm',
    SE_3 =          '10Y1001A1001A46L', 'SE3 BZ / MBA',                                 'Europe/Stockholm',
    SE_4 =          '10Y1001A1001A47J', 'SE4 BZ / MBA',                                 'Europe/Stockholm',
    RS =            '10YCS-SERBIATSOV', 'Serbia, EMS BZ / CA / MBA',                    'Europe/Belgrade',
    SK =            '10YSK-SEPS-----K', 'Slovakia, SEPS BZ / CA / MBA',                 'Europe/Bratislava',
    SI =            '10YSI-ELES-----O', 'Slovenia, ELES BZ / CA / MBA',                 'Europe/Ljubljana',
    GB_NIR =        '10Y1001A1001A016', 'Northern Ireland, SONI CA',                    'Europe/Belfast',
    ES =            '10YES-REE------0', 'Spain, REE BZ / CA / MBA',                     'Europe/Madrid',
    SE =            '10YSE-1--------K', 'Sweden, Sweden MBA, SvK CA',                   'Europe/Stockholm',
    CH =            '10YCH-SWISSGRIDZ', 'Switzerland, Swissgrid BZ / CA / MBA',         'Europe/Zurich',
    DE_TENNET =     '10YDE-EON------1', 'TenneT GER CA',                                'Europe/Berlin',
    DE_TRANSNET =   '10YDE-ENBW-----N', 'TransnetBW CA',                                'Europe/Berlin',
    TR =            '10YTR-TEIAS----W', 'Turkey BZ / CA / MBA',                         'Europe/Istanbul',
    UA =            '10Y1001C--00003F', 'Ukraine, Ukraine BZ, MBA',                     'Europe/Kiev',
    UA_DOBTPP =     '10Y1001A1001A869', 'Ukraine-DobTPP CTA',                           'Europe/Kiev',
    UA_BEI =        '10YUA-WEPS-----0', 'Ukraine BEI CTA',                              'Europe/Kiev',
    UA_IPS =        '10Y1001C--000182', 'Ukraine IPS CTA',                              'Europe/Kiev'
