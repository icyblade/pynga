import pytest

from pynga.forum import SubForum
from pynga.session import Session
from pynga.thread import Thread

STID = 11477435
AUTHENTICATION = {'uid': 42099452, 'cid': 'Z8gabrmhdt8j87am7dht5adhenps6sq801kc9gbl'}


def test_init():
    session = Session()
    SubForum(STID, session=session)
    with pytest.raises(ValueError, message='session should be specified.'):
        SubForum(STID)
    with pytest.raises(NotImplementedError, message='Slow query is now supported yet.'):
        SubForum(STID, session=session, page_limit=1000)


def test_repr():
    session = Session()
    assert repr(SubForum(STID, session=session)) == '<pynga.forum.SubForum, stid=11477435>'


def test_threads():
    session = Session(AUTHENTICATION)
    sub_forum = SubForum(STID, session=session, page_limit=2)

    assert 11343942 in sub_forum.threads.keys()
    for tid, thread in sub_forum.threads.items():
        assert isinstance(thread, Thread)
        assert thread.tid == tid
