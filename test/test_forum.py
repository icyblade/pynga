import pytest

from pynga.forum import Forum
from pynga.session import Session
from pynga.thread import Thread

FID = 335
AUTHENTICATION = {'uid': 42099452, 'cid': 'Z8gabrmhdt8j87am7dht5adhenps6sq801kc9gbl'}


def test_init():
    session = Session()
    Forum(FID, session=session)
    with pytest.raises(ValueError, message='session should be specified.'):
        Forum(FID)
    with pytest.raises(NotImplementedError, message='Slow query is now supported yet.'):
        Forum(FID, session=session, page_limit=1000)


def test_repr():
    session = Session()
    assert repr(Forum(FID, session=session)) == '<pynga.forum.Forum, fid=335>'


def test_threads():
    session = Session(AUTHENTICATION)
    forum = Forum(FID, session=session, page_limit=5)

    assert 8135880 in forum.threads.keys()
    for tid, thread in forum.threads.items():
        assert isinstance(thread, Thread)
        assert thread.tid == tid
