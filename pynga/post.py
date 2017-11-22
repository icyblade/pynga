import re

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
    def raw(self):
        return self.session.get_json(f'{HOST}/read.php?pid={self.pid}&lite=js')

    @property
    def user(self):
        try:
            uid = int(self.raw['data']['__R']['0']['authorid'])
        except KeyError:
            uid = None
        if uid == -1:  # anonymous user
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

    @property
    def alterinfo(self):
        alterinfo_raw = self.raw['data']['__R']['0']['alterinfo']
        alterinfo_extracted = map(
            lambda x: x.split(' '),
            re.findall('\[(.+?)\]', alterinfo_raw)
        )
        for alterinfo in alterinfo_extracted:
            action = alterinfo[0][0]
            if action == 'E':  # edit
                assert len(alterinfo) == 3
                assert alterinfo[1] == alterinfo[2] == '0'
                yield {
                    'action': action,
                    'edit_timestamp': int(alterinfo[0][1:])
                }
            elif action == 'A':  # add point
                assert 4 <= len(alterinfo) <= 5
                yield {
                    'action': action,
                    'reputation': int(alterinfo[0][1:]),  # 声望
                    'rvrc': float(alterinfo[1]),  # 威望
                    'gold': float(alterinfo[2]),  # 金钱
                    'log_id': int(alterinfo[3]),
                    'info': alterinfo[4] if len(alterinfo) == 5 else '',
                }
            elif action == 'U':  # undo
                assert len(alterinfo) == 3
                yield {
                    'action': action,
                    'reputation': int(alterinfo[0][1:]),  # 声望
                    'rvrc': float(alterinfo[1]),  # 威望
                    'gold': float(alterinfo[2]),  # 金钱
                }
            else:
                raise ValueError(f'Invalid action: {action}')

    def add_point(self, value, info='', options=None):  # pragma: no cover
        """回复加分接口

        Parameters
        --------
        value: int.
            加分声望值.
        info: str. (Default: '')
            加分说明.
        options: list of str. (Default: None)
            加分相关选项.
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
