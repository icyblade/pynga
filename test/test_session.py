import re

import pytest

from pynga.session import Session


def test_init():
    # test plain session
    Session()
    Session(max_retries=10)
    Session({'uid': 123, 'cid': 'abc'})
    with pytest.raises(ValueError, message='dict or None expected, found str.'):
        Session('invalid_authentication')
    with pytest.raises(NotImplementedError, message='Login with username/password is not implemented yet.'):
        Session({'username': 'username', 'password': 'p@ssw0rd'})
    with pytest.raises(NotImplementedError, message='Login with username/password is not implemented yet.'):
        Session({'uid': 123, 'cid': 'abc', 'username': 'username', 'password': 'p@ssw0rd'})

    # test max_retries
    with pytest.raises(ValueError, message='int expected, found str.'):
        Session(max_retries='test')
    with pytest.raises(ValueError, message='max_retries should be greater or equal to 1.'):
        ValueError, Session(max_retries=-1)


def test_http_get():
    session = Session()

    text = session.get_text('http://bbs.ngacn.cc/thread.php?fid=7')
    regex_result = re.findall('<title>([\S\s]+?)</title>', text)
    assert regex_result == ['艾泽拉斯议事厅 - Hall of Azeroth']

    html = session.get_html('http://bbs.ngacn.cc/thread.php?fid=7')
    assert html.title.text == '艾泽拉斯议事厅 - Hall of Azeroth'

    json_data = session.get_json('http://bbs.ngacn.cc/thread.php?fid=7&lite=js')
    assert json_data['data']['__F']['fid'] == 7
