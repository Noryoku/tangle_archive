import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class HttpRequest:
    def __init__(self, method, url, data=None, headers=None, auth=None, timeout=10):
        self.headers = headers
        self.auth = auth
        self.data = data
        self.timeout = timeout
        self.url = url

        self.make_request(method)

    def _requests_retry_session(self, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
        method_whitelist = ["GET", "PUT", "POST", "DELETE"]
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            method_whitelist=method_whitelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def make_request(self, method):
        return self._requests_retry_session().request(
            method,
            self.url,
            data=self.data,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
            verify=False
        )

