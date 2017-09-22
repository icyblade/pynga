import json

import requests
from bs4 import BeautifulSoup

NGA_JSON_SHIFT = len('window.script_muti_get_var_store=')

class Session(object):
    def __init__(self, authentication=None, max_retries=5, timeout=5):
        self._build_session(authentication, max_retries)
        self.timeout = timeout

    def _build_session(self, authentication, max_retries):
        from requests.adapters import HTTPAdapter

        if not isinstance(max_retries, int):
            raise ValueError(f'int expected, found {type(max_retries)}.')
        elif max_retries < 1:
            raise ValueError('max_retries should be greater or equal to 1.')

        # mount retries adapter
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=max_retries))

        # update authentication
        if isinstance(authentication, dict):
            if 'uid' in authentication and 'cid' in authentication:
                session.headers.update({
                    'Cookie': f'ngaPassportUid={authentication["uid"]}; ngaPassportCid={authentication["cid"]};'
                })
            if 'username' in authentication and 'password' in authentication:
                raise NotImplementedError('Login with username/password is not implemented yet.')
        elif authentication is None:
            pass
        else:
            raise ValueError(f'dict or None expected, found {type(authentication)}.')

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

