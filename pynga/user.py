from pynga.default_config import HOST


class User(object):
    def __init__(self, uid=None, username=None, session=None):
        self.uid = uid
        self.username = username
        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')
        self._validate_user()

    def __repr__(self):
        return f'<pynga.user.User, uid={self.uid}>'

    def __eq__(self, user):
        return self.uid == user.uid

    def _validate_user(self):
        if self.username is not None:
            json_data = self.session.get_json(f'{HOST}/nuke.php?__lib=ucp&__act=get&lite=js&username={self.username}')

            # extract uid
            if 'error' in json_data:
                raise Exception(json_data['error']['0'])
            uid = int(json_data['data']['0']['uid'])

            if self.uid is not None and self.uid != uid:
                raise ValueError(f'User {self.username} should have UID {uid} rather than {self.uid}.')
            else:
                self.uid = uid
        elif self.uid is not None:
            json_data = self.session.get_json(f'{HOST}/nuke.php?__lib=ucp&__act=get&lite=js&uid={self.uid}')

            # extract username
            if 'error' in json_data:
                raise Exception(json_data['error']['0'])
            username = json_data['data']['0']['username']

            self.username = username
        else:
            # anonymous user
            pass

    def _validate_current_user(self):
        if self.session.authentication['uid'] != self.uid:
            raise RuntimeError('Only current user can use this method.')

    def undo_log(self, log_id):  # pragma: no cover
        """撤销操作记录

        Parameters
        --------
        log_id: int.
            操作记录 ID.
        """
        self._validate_current_user()
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?__lib=undo&__act=undo&raw=3&logid={log_id}&lite=js',
            {'nouse': 'post'},
        )

        return json_data

    def buy_item(self, item_id):  # pragma: no cover
        """从系统商店购买物品.

        Parameters
        --------
        item_id: int.
            物品 ID.
        """
        self._validate_current_user()
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?func=item&act=buy&raw=3&lite=js',
            {'id': item_id, 'count': 1}
        )

        return json_data

    def use_item(self, inventory_id, uid):  # pragma: no cover
        """使用物品

        Parameters
        --------
        inventory_id: int.
            仓库内物品 ID.
        uid: int.
            目标 UID.
        """
        self._validate_current_user()
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?func=item&act=use&raw=3&lite=js',
            {'id': inventory_id, 'arg': uid}
        )

        return json_data
