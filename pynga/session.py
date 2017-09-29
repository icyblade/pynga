import json

import requests
from bs4 import BeautifulSoup
from cachecontrol import CacheControlAdapter
from cachecontrol.heuristics import ExpiresAfter
from urllib3.util.retry import Retry

from pynga.default_config import USER_AGENT

NGA_JSON_SHIFT = len('window.script_muti_get_var_store=')


class Session(object):
    def __init__(self, authentication=None, max_retries=5, timeout=5):
        self.authentication = authentication
        self._build_session(max_retries)
        self.timeout = timeout

    def _build_session(self, max_retries):
        from requests.adapters import HTTPAdapter

        if not isinstance(max_retries, int):
            raise ValueError(f'int expected, found {type(max_retries)}.')
        elif max_retries < 1:
            raise ValueError('max_retries should be greater or equal to 1.')

        session = requests.Session()

        # mount retries adapter
        session.mount('http://', HTTPAdapter(max_retries=Retry(
            total=max_retries, method_whitelist=frozenset(['GET', 'POST'])
        )))

        # mount cache adapter
        session.mount('http://', CacheControlAdapter(heuristic=ExpiresAfter(hours=1)))

        # update authentication
        if isinstance(self.authentication, dict):
            if 'uid' in self.authentication and 'cid' in self.authentication:
                session.headers.update({
                    'Cookie': (
                        f'ngaPassportUid={self.authentication["uid"]};'
                        f'ngaPassportCid={self.authentication["cid"]};'
                    )
                })
            if 'username' in self.authentication and 'password' in self.authentication:
                raise NotImplementedError('Login with username/password is not implemented yet.')
        elif self.authentication is None:
            pass
        else:
            raise ValueError(f'dict or None expected, found {type(self.authentication)}.')

        session.headers['User-Agent'] = USER_AGENT

        self.session = session

    def _get(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        r = self.session.get(*args, **kwargs)
        r.encoding = 'gbk'
        return r.text

    def get_text(self, *args, **kwargs):
        text = self._get(*args, **kwargs)
        return text

    def get_html(self, *args, **kwargs):
        text = self._get(*args, **kwargs)
        html = BeautifulSoup(text, 'html.parser')
        return html

    def get_json(self, *args, **kwargs):
        text = self._get(*args, **kwargs)
        json_data = json.loads(text[NGA_JSON_SHIFT:], strict=False)
        return json_data

    def _post(self, *args, **kwargs):  # pragma: no cover
        kwargs['timeout'] = self.timeout
        r = self.session.post(*args, **kwargs)
        r.encoding = 'gbk'
        return r.text

    def post_read_json(self, *args, **kwargs):  # pragma: no cover
        text = self._post(*args, **kwargs)
        json_data = json.loads(text[NGA_JSON_SHIFT:], strict=False)
        return json_data
