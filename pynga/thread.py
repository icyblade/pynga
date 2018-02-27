from pynga.default_config import HOST
from pynga.misc import handle_alterinfo
from pynga.post import Post
from pynga.user import User


class Thread(object):
    def __init__(self, tid, session=None, cache_page=float('inf')):
        self.tid = tid
        self.cache_page = cache_page
        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')

    def __repr__(self):
        return f'<pynga.thread.Thread, tid={self.tid}>'

    @property
    def raw(self):
        from math import ceil

        raw_all = {}
        page = 1
        while page <= self.cache_page:
            raw = self.session.get_json(f'{HOST}/read.php?tid={self.tid}&lite=js&page={page}')
            raw_all[page] = raw
            n_pages = ceil(raw['data']['__ROWS'] / raw['data']['__R__ROWS_PAGE'])
            if page < n_pages:
                page += 1
            else:
                break

        return raw_all

    @property
    def n_pages(self):
        return len(self.raw)

    @property
    def user(self):
        uid = int(self.raw[1]['data']['__T']['authorid'])
        return User(uid=uid, session=self.session)

    @property
    def subject(self):
        return self.raw[1]['data']['__T']['subject']

    @property
    def content(self):
        return self.raw[1]['data']['__R']['0']['content']  # the thread itself is a special posts

    @property
    def posts(self):
        from collections import OrderedDict

        posts = OrderedDict([])
        for page, raw in self.raw.items():
            # process posts
            for _, post_raw in raw['data']['__R'].items():
                if 'pid' in post_raw:  # posts
                    posts[post_raw['lou']] = Post(post_raw['pid'], session=self.session)
                else:
                    posts[post_raw['lou']] = Post(None, session=self.session)

        assert posts[0].pid == 0, 'Unknown error.'
        posts[0] = self

        return posts

    def move(self, target_forum, pm=True, pm_message='', push=True):  # pragma: no cover
        """移动帖子.

        Parameters
        --------
        target_forum: instance of pynga.forum.Forum.
            目标版面.
        pm: bool. (Default: True)
            是否 PM.
        pm_message: str. (Default: '')
            PM 消息内容.
        push: bool. (Default: True)
            是否提前帖子.

        Returns
        --------
        json_data: dict.
            Response in JSON dict.
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
        alterinfo_raw = self.raw[1]['data']['__R']['0']['alterinfo']
        return handle_alterinfo(alterinfo_raw)
