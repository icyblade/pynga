from datetime import datetime
from random import random

import pytest

from pynga.session import Session
from pynga.user import User

UID = 42099452
USERNAME = 'pynga_test_01'
AUTHENTICATION = {'uid': 42099452, 'cid': 'Z8gabrmhdt8j87am7dht5adhenps6sq801kc9gbl'}


def test_init():
    session = Session()

    with pytest.raises(ValueError, message='session should be specified.'):
        User()

    User(session=session)

    user = User(uid=UID, session=session)
    assert user.username == 'pynga_test_01'

    user = User(username=USERNAME, session=session)
    assert user.uid == 42099452
    assert user.__hash__() == UID.__hash__()

    User(uid=UID, username=USERNAME, session=session)

    with pytest.raises(ValueError, message='User pynga_test_01 should have UID 42099452 rather than 99999999.'):
        User(uid=99999999, username=USERNAME, session=session)

    with pytest.raises(Exception, message='找不到用户'):
        User(username='this is an invalid username', session=session)

    with pytest.raises(Exception, message='找不到用户'):
        User(uid=99999999, session=session)


def test_repr():
    session = Session()
    user = User(uid=UID, session=session)
    assert repr(user) == '<pynga.user.User, uid=42099452>'


def test_operator():
    session = Session()
    user = User(uid=UID, session=session)
    same_user = User(uid=UID, session=session)
    another_user = User(uid=58, session=session)
    assert user == same_user
    assert user != another_user


def test_anonymous_user():
    session = Session()
    user = User(uid=-1, session=session)
    assert user.is_anonymous
    user = User(uid=None, session=session)
    assert user.is_anonymous


def test_sign():
    session = Session({'uid': AUTHENTICATION['uid'], 'cid': AUTHENTICATION['cid']})
    user = User(uid=42099452, session=session)
    sign = f'中文测试签名 {random()}'
    user.sign = sign
    assert user.sign == sign

    user = User(uid=-1, session=session)
    assert user.sign is None


def test_register_date():
    session = Session()
    user = User(uid=UID, session=session)
    assert user.register_date == datetime(2017, 9, 19, 10, 21, 30)

    user = User(uid=-1, session=session)
    assert user.register_date is None


def test_chinese_username():
    session = Session()
    user = User(username='清风善堂', session=session)
    assert user.uid == 1742851
