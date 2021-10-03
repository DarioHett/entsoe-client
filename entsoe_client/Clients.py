import logging
from typing import Optional, Dict

import requests
import tenacity
from entsoe_client.Queries import Query
from lxml import etree

URL = "https://transparency.entsoe.eu/api"
retry_count = 1


class Client:
    # noinspection LongLine
    """
    Basic GET Request interface to ENTSOE API.
    Requires an API Key for access.

    `_request` parses a Dict for the API call.

    Documentation:
    https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_request_methods
    """

    def __init__(
        self,
        api_key: str,
        session: Optional[requests.Session] = None,
        proxies: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        if api_key:
            self.api_key = api_key
        else:
            raise AttributeError
        self.session = session if session else requests.Session()
        self.proxies = proxies
        self.timeout = timeout

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(retry_count),
        wait=tenacity.wait_fixed(1),
        reraise=True,
    )
    def _request(self, params: Dict) -> requests.Response:
        params.update({"securityToken": self.api_key})

        logging.debug(f"{params}")
        response = self.session.get(
            url=URL, params=params, proxies=self.proxies, timeout=self.timeout
        )

        return response

    @staticmethod
    def _validate_response(response: requests.Response) -> requests.Response:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            response_xml = "\n".join(
                response.text.split("\n")[1:]
            )  # Drop encoding <?...?>
            response_etree = etree.fromstring(response_xml)
            reason = response_etree.find(".//Reason/text", response_etree.nsmap)
            logging.debug("Response Reason: " + reason.text)
            return response
        else:
            return response

    def download(self, query: Query) -> requests.Response:
        params: Dict = query()
        response: requests.Response = self._request(params)
        validated_response = self._validate_response(response)
        return validated_response

    def __call__(self, query: Query):
        return self.download(query)
