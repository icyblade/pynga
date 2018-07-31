import datetime
import json
from urllib.parse import quote

import pytz

from pynga.default_config import ADMIN_LOG_TYPE_MAPPER, HOST, TIMEZONE


class User(object):
    """NGA 用户基础类.

    支持根据 UID 或用户名来指定用户. 如果二者都没有进行指定, 则定义为匿名用户.
    匿名用户的 UID 和用户名定义为 None, 反之亦然.

    Parameters
    --------
    uid: int
        用户的 UID. 默认: None.
    username: str
        用户的用户名. 默认: None.
    session: :class:`Session <pynga.session.Session>`
        获取数据所使用的 session.
    """
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
    def is_anonymous(self) -> bool:
        """获取用户的匿名状态."""
        return self.uid is None

    @staticmethod
    def _timestamp_to_datetime(timestamp):
        """在 UTC+8 时区下, 将时间戳转化为无 tz 的 datetime 对象.

        Parameters
        --------
        timestamp: int.

        Returns
        --------
        dt: instance of datetime.datetime.
        """
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone(TIMEZONE)).replace(tzinfo=None)
        return dt

    @property
    def register_date(self) -> datetime.datetime:
        """获取用户的注册日期及时间."""
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
    def sign(self) -> str:
        """获取用户的签名.

        也可以通过 setter 来设置签名.
        """
        if self.is_anonymous:
            return None
        else:
            json_data = self.session.post_read_json(
                f'{HOST}/nuke.php',
                {'__lib': 'set_sign', '__act': 'get', 'uid': self.uid, 'lite': 'js'}
            )

            return str(json_data['data']['0'])

    @sign.setter
    def sign(self, value):
        """设置用户的签名.

        Parameters
        --------
        value: str
            需要设置的签名.

        Raises
        --------
        ValueError: 服务器返回的报错信息.
        """
        if not self.is_anonymous:
            json_data = self.session.post_read_json(
                f'{HOST}/nuke.php',
                {
                    '__lib': 'set_sign', '__act': 'set',
                    'uid': self.uid, 'lite': 'js', 'sign': value.encode('gbk'),
                    'disable': '',
                }
            )

            if 'error' in json_data:
                raise ValueError(json_data['error']['0'])
            else:
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

        Parameters
        --------
        type: str
            操作记录类型名称.

        Yields
        --------
        :class:`AdminLog <pynga.user.AdminLog>`.
            操作记录对象.
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

    def undo_admin_log(self, admin_log):  # pragma: no cover
        """撤销操作记录.

        Parameters
        --------
        admin_log: :class:`AdminLog <pynga.user.AdminLog>`
            需要撤销的操作记录.
        """
        self._validate_current_user()
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?__lib=undo&__act=undo&raw=3&logid={admin_log.log_id}&lite=js',
            {'nouse': 'post'},
        )

        return json_data

    def buy_item(self, item_id):  # pragma: no cover
        """从系统商店购买物品.

        Parameters
        --------
        item_id: int.
            购买的物品 ID.

        Returns
        --------
        dict
            服务器返回的 JSON, 以 dict 的形式.
        """
        self._validate_current_user()
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?func=item&act=buy&raw=3&lite=js',
            {'id': item_id, 'count': 1}
        )

        return json_data

    def use_item(self, inventory_id, user):  # pragma: no cover
        """使用物品.

        Parameters
        --------
        inventory_id: int
            仓库内物品 ID.
        user: :class:`User <pynga.user.User>`
            使用物品的目标用户对象.
        """
        self._validate_current_user()
        json_data = self.session.post_read_json(
            f'{HOST}/nuke.php?func=item&act=use&raw=3&lite=js',
            {'id': inventory_id, 'arg': user.uid}
        )

        return json_data


class AdminLog(object):
    """NGA 操作记录基础类.

    Parameters
    --------
    data: str or dict
        操作记录 JSON, 以 str 或 dict 的形式.
    admin_log_type_mapper: dict
        操作记录映射表, 一般由服务器提供.
    """
    def __init__(self, data, admin_log_type_mapper=None):
        if isinstance(data, dict):
            self.raw = data
        else:
            self.raw = json.loads(data)
        self.admin_log_type_mapper = admin_log_type_mapper if admin_log_type_mapper else ADMIN_LOG_TYPE_MAPPER

    def __repr__(self):
        return f'<pynga.user.AdminLog, id={self.log_id}>'

    @property
    def log_id(self) -> int:
        """操作记录 ID."""
        return int(self.raw['0'])

    @property
    def type(self) -> str:
        """操作记录类型."""
        return self.admin_log_type_mapper[str(self.raw['1'])]

    @property
    def source_uid(self) -> int:
        """操作人 UID."""
        return int(self.raw['2'])

    @property
    def target_uid(self) -> int:
        """被操作人 UID."""
        return int(self.raw['3'])

    @property
    def tid(self) -> int:
        """操作记录对应的 TID."""
        return int(self.raw['4'])

    @property
    def message(self) -> str:
        """操作信息."""
        return str(self.raw['5'])

    @property
    def time(self) -> datetime.datetime:
        """操作时间."""
        return User._timestamp_to_datetime(self.raw['6'])
