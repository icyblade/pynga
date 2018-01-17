import re

from pynga.default_config import HOST
from pynga.forum import Forum, SubForum
from pynga.post import Post
from pynga.session import Session
from pynga.thread import Thread
from pynga.user import User


class NGA(object):
    """NGA 基础类.

    Parameters
    --------
    authentication: dict.
        支持的 key 包括 uid, username, cid.
    max_retries: int. (Default: 5)
        请求最多重试的次数.
    """

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
        """定义一个 NGA 用户.

        用户的 uid 和 username 至少需要指定一个, 否则是匿名用户.

        Parameters
        --------
        uid: int. (Default: None)
            用户的 UID.
        username: string. (Default: None)
            用户的用户名.

        Returns
        --------
        user: instance of pynga.user.User.
        """
        return User(uid=uid, username=username, session=self.session)

    def Post(self, pid):
        """定义一个回复.

        Parameters
        --------
        pid: int.
            回复的 PID.

        Returns
        --------
        post: instance of pynga.post.Post.
        """
        return Post(pid, session=self.session)

    def Thread(self, tid):
        """定义一个帖子.

        Parameters
        --------
        tid: int.
            帖子的 TID.

        Returns
        --------
        thread: instance of pynga.thread.Thread.
        """
        return Thread(tid, session=self.session)

    def Forum(self, fid):
        """定义一个版面.

        Parameters
        --------
        fid: int.
            版面的 FID.

        Returns
        --------
        forum: instance of pynga.forum.Forum.
        """
        return Forum(fid, session=self.session)

    def SubForum(self, stid):
        """定义一个合集.

        Parameters
        --------
        stid: int.
            合集的 STID.

        Returns
        --------
        sub_forum: instance of pynga.forum.SubForum.
        """
        return SubForum(stid, session=self.session)
