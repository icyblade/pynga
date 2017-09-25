import pytest

from pynga.session import Session
from pynga.user import User

UID = 42099452
USERNAME = 'pynga_test_01'


def test_init():
    session = Session()

    with pytest.raises(ValueError, message='session should be specified.'):
        User()

    User(session=session)

    user = User(uid=UID, session=session)
    assert user.username == 'pynga_test_01'

    user = User(username=USERNAME, session=session)
    assert user.uid == 42099452

    User(uid=UID, username=USERNAME, session=session)

    with pytest.raises(ValueError, message='User pynga_test_01 should have UID 42099452 rather than 99999999.'):
        User(uid=99999999, username=USERNAME, session=session)

    with pytest.raises(Exception, message='找不到用户'):
        User(username='this is an invalid username', session=session)

    with pytest.raises(Exception, message='找不到用户'):
        User(uid=99999999, session=session)
