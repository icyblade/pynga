import json
import re

import requests
from bs4 import BeautifulSoup
from cachecontrol import CacheControlAdapter
from cachecontrol.heuristics import ExpiresAfter
from urllib3.util.retry import Retry

from pynga.default_config import USER_AGENT

NGA_JSON_SHIFT = len('window.script_muti_get_var_store=')


class Session(object):
    """NGA Session 基础类.

    Parameters
    --------
    authentication: dict
        登陆信息, 支持的 key 包括 uid, username, cid.
        其中 cid 为必须的 key, uid 和 username 至少需要指定一个.
    max_retries: int
        最大重试次数. 默认: 5.
    timeout: int
        超时时间, 以秒为单位. 默认: 5.
    max_workers: int
        并行度. 默认: 1.
    """
    def __init__(self, authentication=None, max_retries=5, timeout=5, max_workers=1):
        if authentication is None:
            self.authentication = {'guestJs': 1526554662}
        else:
            self.authentication = authentication
        self._build_session(max_retries, max_workers)
        self.timeout = timeout

    def _build_session(self, max_retries, max_workers):
        if not isinstance(max_retries, int):
            raise ValueError(f'int expected, found {type(max_retries)}.')
        elif max_retries < 1:
            raise ValueError('max_retries should be greater or equal to 1.')

        session = requests.Session()

        # mount cache adapter with retries
        session.mount(
            'http://',
            CacheControlAdapter(
                max_retries=Retry(
                    total=max_retries, method_whitelist=frozenset(['GET', 'POST'])
                ),
                heuristic=ExpiresAfter(hours=1)
            )
        )

        # update authentication
        if isinstance(self.authentication, dict):
            if 'uid' in self.authentication and 'cid' in self.authentication:
                session.headers.update({
                    'Cookie': (
                        f'ngaPassportUid={self.authentication["uid"]};'
                        f'ngaPassportCid={self.authentication["cid"]};'
                    )
                })
            elif 'guestJs' in self.authentication:
                session.headers.update({
                    'Cookie': (
                        f'guestJs={self.authentication["guestJs"]};'
                    )
                })
            elif 'username' in self.authentication and 'password' in self.authentication:
                raise NotImplementedError('Login with username/password is not implemented yet.')
        elif self.authentication is None:
            pass
        else:
            raise ValueError(f'dict or None expected, found {type(self.authentication)}.')

        session.headers['User-Agent'] = USER_AGENT

        if max_workers == 1:
            self.session = session
        else:
            raise NotImplementedError()

    def _get(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        r = self.session.get(*args, **kwargs)
        r.encoding = 'gbk'
        return r.text

    def get_text(self, *args, **kwargs) -> str:
        """发送 GET 请求并获取纯文本返回."""
        text = self._get(*args, **kwargs)
        return text

    def get_html(self, *args, **kwargs) -> BeautifulSoup:
        """发送 GET 请求并获取 HTML 返回."""
        text = self._get(*args, **kwargs)
        html = BeautifulSoup(text, 'html.parser')
        return html

    def get_json(self, *args, **kwargs) -> dict:
        """发送 GET 请求并获取 JSON 返回."""
        text = self._get(*args, **kwargs)
        data = re.sub(r'\\x([0-9A-F]{2})', r'\\u00\1', text[NGA_JSON_SHIFT:])  # patch \x?? illegal escape
        json_data = json.loads(data, strict=False)
        return json_data

    def _post(self, *args, **kwargs):  # pragma: no cover
        kwargs['timeout'] = self.timeout
        r = self.session.post(*args, **kwargs)
        r.encoding = 'gbk'
        return r.text

    def post_read_json(self, *args, **kwargs) -> dict:  # pragma: no cover
        """发送 POST 请求并获取 JSON 返回."""
        text = self._post(*args, **kwargs)
        json_data = json.loads(text[NGA_JSON_SHIFT:], strict=False)
        return json_data
