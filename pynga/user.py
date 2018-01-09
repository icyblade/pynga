import json
from datetime import datetime
from urllib.parse import quote

import pytz

from pynga.default_config import ADMIN_LOG_TYPE_MAPPER, HOST, TIMEZONE


class User(object):
    def __init__(self, uid=None, username=None, session=None):
        self.uid = uid
        self.username = username
        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')
        self._validate_user()

    def __hash__(self):
        return self.uid.__hash__()

    def __repr__(self):
        return f'<pynga.user.User, uid={self.uid}>'

    def __eq__(self, other):
        return self.uid == other.uid

    def __ne__(self, other):
        return self.uid != other.uid

    @property
    def is_anonymous(self):
        return self.uid is None

    @staticmethod
    def _timestamp_to_datetime(timestamp):
        """在 UTC+8 时区下，将时间戳转化为无 tz 的 datetime 对象.

        Parameters
        --------
        timestamp: int.

        Returns
        --------
        dt: instance of datetime.datetime.
        """
        dt = datetime.fromtimestamp(timestamp, tz=pytz.timezone(TIMEZONE)).replace(tzinfo=None)
        return dt

    @property
    def register_date(self):
        if self.is_anonymous:
            return None
        else:
            json_data = self.session.post_read_json(
                f'{HOST}/nuke.php',
                {'__lib': 'ucp', '__act': 'get', 'lite': 'js', 'uid': self.uid}
            )

            timestamp = json_data['data']['0']['regdate']
            register_date = self._timestamp_to_datetime(int(timestamp))

            return register_date

    @property
    def sign(self):
        if self.is_anonymous:
            return None
        else:
            json_data = self.session.post_read_json(
                f'{HOST}/nuke.php',
                {'__lib': 'set_sign', '__act': 'get', 'uid': self.uid, 'lite': 'js'}
            )

            return json_data['data']['0']

    @sign.setter
    def sign(self, value):
        if not self.is_anonymous:
            json_data = self.session.post_read_json(
                f'{HOST}/nuke.php',
                {
                    '__lib': 'set_sign', '__act': 'set',
                    'uid': self.uid, 'lite': 'js', 'sign': value.encode('gbk'),
                    'disable': '',
                }
            )

            assert json_data['data']['0'] == '操作成功'

    def _validate_user(self):
        if self.uid == -1:  # anonymous user
            self.uid = None

        if self.username is not None:
            json_data = self.session.get_json(
                f'{HOST}/nuke.php?__lib=ucp&__act=get&lite=js&username={quote(self.username.encode("gbk"))}'
            )

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

    def get_admin_log(self, type=None):  # pragma: no cover
        """获取当前用户的操作记录.


        Yields
        --------
        log: instance of pynga.user.AdminLog.
        """
        id = None
        if type is None:
            id = ''
        else:
            for type_id, type_name in ADMIN_LOG_TYPE_MAPPER.items():
                if type_name == type:
                    id = type_id
                    break
        if id is None:
            raise ValueError(f'Unknown admin type {type}.')

        page = 1
        while True:
            json_data = self.session.post_read_json(
                f'{HOST}/nuke.php?__lib=admin_log_search&__act=search&from={self.uid}&to=&id=&lite=js',
                {'type': id, 'about': '', 'raw': 3, 'page': page},
            )

            if not len(json_data['data']['0']):
                break

            for _, raw in json_data['data']['0'].items():
                yield AdminLog(json.dumps(raw), json_data['data']['2'])

            page += 1

    def undo_admin_log(self, log_id):  # pragma: no cover
        """撤销操作记录.

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
        """使用物品.

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


class AdminLog(object):
    """操作记录.

    Parameters
    --------
    data: str
        JSON data represented in str. For example: {
            "0": log_id,
            "1": type,
            "2": source_uid,
            "3": target_uid,
            "4": tid,
            "5": admin_log_message,
            "6": timestamp,
        }
    """
    def __init__(self, data, admin_log_type_mapper=ADMIN_LOG_TYPE_MAPPER):
        self.raw = data
        self.raw_json = json.loads(self.raw)
        self.admin_log_type_mapper = admin_log_type_mapper

    def __repr__(self):
        return f'<pynga.user.AdminLog, id={self.log_id}>'

    @property
    def log_id(self):
        return int(self.raw_json['0'])

    @property
    def type(self):
        return self.admin_log_type_mapper[str(self.raw_json['1'])]

    @property
    def source_uid(self):
        return int(self.raw_json['2'])

    @property
    def target_uid(self):
        return int(self.raw_json['3'])

    @property
    def tid(self):
        return int(self.raw_json['4'])

    @property
    def message(self):
        return self.raw_json['5']

    @property
    def time(self):
        return User._timestamp_to_datetime(self.raw_json['6'])
