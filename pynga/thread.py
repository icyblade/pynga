from pynga.default_config import HOST
from pynga.misc import handle_alterinfo
from pynga.post import Post
from pynga.user import User


class Thread(object):
    """NGA 帖子基础类.

    Parameters
    --------
    tid: int
        帖子的 TID.
    session: :class:`Session <pynga.session.Session>`
        获取数据所使用的 session.
    page_limit: int
        最大页面数量. 默认: 无限.
    """
    def __init__(self, tid, session=None, page_limit=float('inf')):
        self.tid = tid
        self.page_limit = page_limit
        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')

    def __repr__(self):
        return f'<pynga.thread.Thread, tid={self.tid}>'

    @property
    def _raw(self):
        from math import ceil

        raw_all = {}
        page = 1
        while page <= self.page_limit:
            raw = self.session.get_json(f'{HOST}/read.php?tid={self.tid}&lite=js&page={page}')
            raw_all[page] = raw
            n_pages = ceil(raw['data']['__ROWS'] / raw['data']['__R__ROWS_PAGE'])
            if page < n_pages:
                page += 1
            else:
                break

        return raw_all

    @property
    def n_pages(self) -> int:
        """获取帖子的总页数."""
        return len(self._raw)

    @property
    def user(self) -> User:
        """获取帖子的发帖人."""
        uid = int(self._raw[1]['data']['__T']['authorid'])
        return User(uid=uid, session=self.session)

    @property
    def subject(self) -> str:
        """获取帖子的标题."""
        return str(self._raw[1]['data']['__T']['subject'])

    @property
    def content(self) -> str:
        """获取帖子的内容.

        注意: 只有主楼的内容会被返回.
        """
        return str(self._raw[1]['data']['__R']['0']['content'])  # the thread itself is a special posts

    @property
    def posts(self):
        """获取帖子的回复.

        注意: 不包括主楼.

        Returns
        --------
        OrderedDict(帖子楼层, :class:`Post <pynga.post.Post>`)
            帖子的回复.
        """
        from collections import OrderedDict

        posts = OrderedDict([])
        for page, raw in self._raw.items():
            # process posts
            for _, post_raw in raw['data']['__R'].items():
                if post_raw['lou'] == 0:  # skip main floor
                    continue
                if 'pid' in post_raw:  # posts
                    posts[post_raw['lou']] = Post(post_raw['pid'], session=self.session)
                else:  # comments, etc
                    posts[post_raw['lou']] = Post(None, session=self.session)

        return posts

    def move(self, target_forum, pm=True, pm_message='', push=True):  # pragma: no cover
        """移动帖子.

        注意: 需要 Moderator 权限.

        Parameters
        --------
        target_forum: :class:`Forum <pynga.forum.Forum>`
            帖子将要移动的目标版面.
        pm: bool
            是否 PM. 默认: True.
        pm_message: str
            PM 消息内容. 默认: 空字符串.
        push: bool
            是否提前帖子. 默认: True.

        Returns
        --------
        dict.
            服务器返回的 JSON, 以 dict 的形式
        """
        if not push:
            op = 2048
        else:
            op = ''
        post_data = {
            '__lib': 'topic_move', '__act': 'move',
            'tid': self.tid, 'fid': target_forum.fid, 'stid': '',
            'pm': int(pm), 'info': pm_message,
            'op': op, 'delay': '', 'raw': 3, 'lite': 'js',
        }

        json_data = self.session.post_read_json(f'{HOST}/nuke.php', post_data)

        return json_data

    @property
    def alterinfo(self):
        """获取帖子的修改/加分/处罚信息.

        Returns
        --------
        list of dict
            该帖子的所有修改/加分/处罚信息.
        """
        alterinfo_raw = self._raw[1]['data']['__R']['0']['alterinfo']
        return handle_alterinfo(alterinfo_raw)
