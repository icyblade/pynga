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

    def undo_log(self, log_id):  # pragma: no cover
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?__lib=undo&__act=undo&raw=3&logid={log_id}&lite=js',
            {'nouse': 'post'},
        )

        return json_data
