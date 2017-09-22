import pytest

from pynga.post import Post
from pynga.session import Session
from pynga.thread import Thread

TID = 7384678

def test_init():
    session = Session()
    Thread(TID, session=session)
    with pytest.raises(ValueError, message='session should be specified.'):
        Thread(TID)

def test_repr():
    session = Session()
    assert repr(Thread(TID, session=session)) == '<pynga.thread.Thread, tid=7384678>'

def test_n_pages():
    session = Session()
    thread = Thread(TID, session=session)
    assert thread.n_pages == 6

def test_user():
    session = Session()
    thread = Thread(TID, session=session)
    assert thread.user.username == 'icyblade'

def test_subject():
    session = Session()
    thread = Thread(TID, session=session)
    assert thread.subject == '[深渊测试团][副本] 6.0 普通/英雄级别团队副本攻略 ---- 悬槌堡'

def test_content():
    session = Session()
    thread = Thread(TID, session=session)
    assert thread.content.find('悬槌堡是高里亚帝国的权力核心') != -1

def test_post():
    session = Session()
    thread = Thread(TID, session=session)
    assert isinstance(thread.posts[0], Thread)
    for i in range(1, len(thread.posts)):
        assert isinstance(thread.posts[i], Post)
    assert [thread.posts[i].pid for i in range(1, 100, 20)] == [
        138914277,
        140035485,
        143215067,
        143426661,
        143467899
    ]
