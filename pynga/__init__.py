import re

from pynga.default_config import HOST
from pynga.post import Post
from pynga.session import Session
from pynga.thread import Thread
from pynga.user import User


class NGA(object):
    def __init__(self, authentication=None, max_retries=5):
        self.session = Session(authentication, max_retries)
        self._set_current_user()

    def _set_current_user(self):
        authentication = self._get_current_user_info()
        self.current_user = self.User(
            uid=authentication['uid'],
            username=authentication['username']
        )

    def _get_current_user_info(self):
        text = self.session.get_text(f'{HOST}')

        # extract uid
        uid = re.findall("__CURRENT_UID = parseInt\('([0-9]*)',10\)", text)
        assert len(uid) == 1
        uid = int(uid[0]) if uid[0] else None

        # extract username
        username = re.findall("__CURRENT_UNAME = '([\s\S]*?)'", text)
        assert len(username) == 1
        username = username[0] if username[0] else None

        return {'uid': uid, 'username': username}

    def User(self, uid=None, username=None):
        return User(uid=uid, username=username, session=self.session)

    def Post(self, pid):
        return Post(pid, session=self.session)

    def Thread(self, tid):
        return Thread(tid, session=self.session)
