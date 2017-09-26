from functools import lru_cache

from pynga.default_config import HOST
from pynga.user import User


class Post(object):
    def __init__(self, pid=None, session=None):
        if pid is not None:
            pid = int(pid)
        self.pid = pid

        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')

    def __repr__(self):
        return f'<pynga.posts.Post, pid={self.pid}>'

    @property
    @lru_cache(1)
    def raw(self):
        return self.session.get_json(f'{HOST}/read.php?pid={self.pid}&lite=js')

    @property
    def user(self):
        try:
            uid = int(self.raw['data']['__R']['0']['authorid'])
        except KeyError:
            uid = None
        return User(uid=uid, session=self.session)

    @property
    def subject(self):
        try:
            return self.raw['data']['__R']['0']['subject']
        except KeyError:
            return None

    @property
    def content(self):
        try:
            return self.raw['data']['__R']['0']['content']
        except KeyError:
            return None

    @property
    def tid(self):
        return int(self.raw['data']['__R']['0']['tid'])

    @property
    def fid(self):
        return int(self.raw['data']['__R']['0']['fid'])

    def add_point(self, value, info='', options=None):  # pragma: no cover
        """回复加分接口

        Parameters
        --------
        value: int.
            加分声望值.
        info: str. (Default: '')
            加分说明.
        """
        value_mapping = {
            15: 16,
            30: 32,
            45: 64,
            60: 128,
            75: 256,
            105: 512,
            150: 1024,
            225: 2048,
            300: 4096,
            375: 8192,
            450: 16384,
            525: 32768,
            600: 65536,
        }
        options_mapping = {
            '增加/扣除金钱': 1, '增加威望': 2,
            '给作者发送PM': 4, '主题加入精华区': 8,
        }

        # validate input
        if options is None:
            options = []
        options = [options] if isinstance(options, str) else options

        assert value in value_mapping
        assert len(set(options)) == len(options)
        assert set(options).issubset(set(options_mapping))

        # calculate opt
        opt = value_mapping[value]
        for key in options:
            opt = opt | options_mapping[key]

        # do requests
        post_data = {
            '__lib': 'add_point_v3', '__act': 'add', 'lite': 'js', 'raw': 3,
            'fid': self.fid, 'tid': self.tid, 'pid': self.pid, 'value': '',
            'opt': opt, 'info': info,
        }

        json_data = self.session.post_read_json(f'{HOST}/nuke.php', post_data)

        return json_data
