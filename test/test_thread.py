import pytest

from pynga.post import Post
from pynga.session import Session
from pynga.thread import Thread

TID = 6406100
AUTHENTICATION = {'uid': 42099452, 'cid': 'Z8gabrmhdt8j87am7dht5adhenps6sq801kc9gbl'}


def test_init():
    session = Session()
    Thread(TID, session=session)
    with pytest.raises(ValueError, message='session should be specified.'):
        Thread(TID)


def test_repr():
    session = Session()
    assert repr(Thread(TID, session=session)) == '<pynga.thread.Thread, tid=6406100>'


def test_n_pages():
    session = Session(AUTHENTICATION)
    thread = Thread(TID, session=session)
    assert thread.n_pages == 2


def test_user():
    session = Session(AUTHENTICATION)
    thread = Thread(TID, session=session)
    assert thread.user.username == 'zeg'


def test_subject():
    session = Session(AUTHENTICATION)
    thread = Thread(TID, session=session)
    assert thread.subject == 'NGA数据接口'


def test_content():
    session = Session(AUTHENTICATION)
    thread = Thread(TID, session=session)
    assert thread.content == '索引占楼'


def test_post():
    session = Session(AUTHENTICATION)
    thread = Thread(TID, session=session)
    assert isinstance(thread.posts[0], Thread)
    for i in range(1, 25):
        assert isinstance(thread.posts[i], Post)
    assert [thread.posts[i].pid for i in range(1, 4)] == [
        115692565, 115692624, 115692689
    ]


def test_alterinfo():
    session = Session(AUTHENTICATION)
    thread = Thread(13333884, session=session)
    expected = {
        'action': 'A',
        'gold': 0.3,
        'info': '',
        'log_id': 18414555,
        'reputation': 30,
        'rvrc': 0.2
    }
    assert expected in list(thread.alterinfo)


def test_cache_page():
    session = Session(AUTHENTICATION)
    thread = Thread(TID, session=session, page_limit=1)
    assert thread.n_pages == 1
