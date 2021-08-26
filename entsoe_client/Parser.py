import requests
import pandas as pd
import entsoe_client.ParserUtils as utils


def parse(response: requests.Response) -> pd.DataFrame:
    """
    Primary function to parse raw Responses to Pandas DataFrames.
    Switch-case functionality for different response content-types.
    TODO: Implement as a class; Factory for Content-Types.
    """
    content = response.headers.get('Content-Type', None)

    if 'documentType=A95' in response.url:
        return utils.parse_masterdata(response)
    elif 'documentType=B11' in response.url:
        return utils.parse_flowbasedparameters(response)
    elif content == 'application/zip':
        return utils.parse_zip(response)
    elif content == 'text/xml':
        return utils.parse_text_xml(response)
    elif content == 'text/xml':
        return utils.parse_text_xml(response)
    else:
        raise NotImplementedError