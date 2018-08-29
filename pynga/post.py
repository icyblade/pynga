from pynga.default_config import HOST
from pynga.misc import handle_alterinfo
from pynga.user import User


class Post(object):
    """NGA 回复基础类.

    如果一个回复不存在 PID, 则定义其为未知回复(例如: 贴条).
    其 PID 定义为 None

    Parameters
    --------
    pid: int
        回复的 PID. 默认: None.
    session: :class:`Session <pynga.session.Session>`
        获取数据所使用的 session.
    """
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

    def __eq__(self, other):
        return self.pid == other.pid

    def __ne__(self, other):
        return self.pid != other.pid

    def __le__(self, other):
        return self.pid <= other.pid

    def __ge__(self, other):
        return self.pid >= other.pid

    def __lt__(self, other):
        return self.pid < other.pid

    def __gt__(self, other):
        return self.pid >= other.pid

    @property
    def _raw(self):
        return self.session.get_json(f'{HOST}/read.php?pid={self.pid}&lite=js')

    @property
    def user(self) -> User:
        """获取回复的回复人."""
        try:
            uid = int(self._raw['data']['__R']['0']['authorid'])
        except KeyError:
            uid = None
        return User(uid=uid, session=self.session)

    @property
    def subject(self) -> str:
        """获取回复的标题."""
        try:
            return str(self._raw['data']['__R']['0']['subject'])
        except KeyError:
            return None

    @property
    def content(self) -> str:
        """获取回复的内容."""
        try:
            return str(self._raw['data']['__R']['0']['content'])
        except KeyError:
            return None

    @property
    def tid(self) -> int:
        """获取回复对应的帖子的 TID."""
        return int(self._raw['data']['__R']['0']['tid'])

    @property
    def fid(self) -> int:
        """获取回复对应的帖子的版面的 FID."""
        return int(self._raw['data']['__R']['0']['fid'])

    @property
    def alterinfo(self):
        """获取回复的修改/加分/处罚信息.

        Returns
        --------
        list of dict
            该回复的所有修改/加分/处罚信息.
        """
        alterinfo_raw = self._raw['data']['__R']['0']['alterinfo']
        return handle_alterinfo(alterinfo_raw)

    def add_point(self, value, info='', options=None):  # pragma: no cover
        """回复加分.

        Parameters
        --------
        value: int
            加分声望值.
        info: str
            加分说明. 默认: 空字符串.
        options: list of str
            加分相关选项. 可选项包括: 增加/扣除金钱, 增加威望, 给作者发送PM, 主题加入精华区. 默认: None
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

    @property
    def attachments(self):
        """获取回复的附件.

        Returns
        --------
        list of dict
        """
        if 'attachs' in self._raw['data']['__R']['0']:
            return list(self._raw['data']['__R']['0']['attachs'].values())
        else:
            return []
