import pytest

from pynga import NGA

AUTHENTICATION = {'uid': 42099452, 'cid': 'Z8gabrmhdt8j87am7dht5adhenps6sq801kc9gbl'}


def test_init():
    NGA()


def test_get_current_user_info():
    nga = NGA()
    assert nga._get_current_user_info() == {'uid': None, 'username': None}

    nga = NGA(AUTHENTICATION)
    assert nga._get_current_user_info() == {'uid': 42099452, 'username': 'pynga_test_01'}


def test_current_user():
    nga = NGA(AUTHENTICATION)
    assert nga.current_user.uid == 42099452
    assert nga.current_user.username == 'pynga_test_01'


def test_user():
    nga = NGA(AUTHENTICATION)
    user = nga.User(42099452)
    assert user.username == 'pynga_test_01'
    user._validate_current_user()

    user = nga.User(5780720)
    with pytest.raises(RuntimeError, message='Only current user can use this method.'):
        user._validate_current_user()


def test_post():
    nga = NGA(AUTHENTICATION)
    post = nga.Post(138966442)
    assert post.user.username == 'icyblade'


def test_thread():
    nga = NGA(AUTHENTICATION)
    thread = nga.Thread(7384678)
    assert thread.user.username == 'icyblade'


def test_forum():
    nga = NGA(AUTHENTICATION)
    nga.Forum(335)


def test_sub_forum():
    nga = NGA(AUTHENTICATION)
    nga.SubForum(11477435)
