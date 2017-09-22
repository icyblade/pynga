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
