import pytest

from pynga.post import Post
from pynga.session import Session

PID = 138966442
AUTHENTICATION = {'uid': 42099452, 'cid': 'Z8gabrmhdt8j87am7dht5adhenps6sq801kc9gbl'}


def test_init():
    session = Session()
    Post(PID, session=session)
    Post(session=session)
    with pytest.raises(ValueError, message='session should be specified.'):
        Post(PID)


def test_repr():
    session = Session()
    assert repr(Post(PID, session=session)) == '<pynga.posts.Post, pid=138966442>'


def test_user():
    session = Session(AUTHENTICATION)
    post = Post(PID, session=session)
    assert post.user.username == 'icyblade'

    post = Post(session=session)
    assert post.user.uid is None
    assert post.user.username is None


def test_subject():
    session = Session(AUTHENTICATION)
    post = Post(PID, session=session)
    assert post.subject == 'test'

    post = Post(session=session)
    assert post.subject is None


def test_content():
    session = Session(AUTHENTICATION)
    post = Post(PID, session=session)
    assert post.content == '占楼占楼占楼占楼占楼占楼占楼占楼<br/>备用楼'

    post = Post(session=session)
    assert post.content is None


def test_tid():
    session = Session(AUTHENTICATION)
    post = Post(PID, session=session)
    assert post.tid == 7384678


def test_fid():
    session = Session(AUTHENTICATION)
    post = Post(PID, session=session)
    assert post.fid == 188


def test_alterinfo():
    session = Session(AUTHENTICATION)
    post = Post(PID, session=session)
    assert list(post.alterinfo) == [
        {'action': 'E', 'by_uid': '0', 'by_username': '0', 'edit_timestamp': 1506041993},
        {'action': 'A', 'reputation': 15, 'rvrc': 0.1, 'gold': 0.15, 'log_id': 12258940, 'info': ''},
        {'action': 'U', 'reputation': -15, 'rvrc': -0.1, 'gold': -0.15},
        {'action': 'A', 'reputation': 15, 'rvrc': 0.1, 'gold': 0.15, 'log_id': 12258960, 'info': 'pynga_test'},
        {'action': 'U', 'reputation': -15, 'rvrc': -0.1, 'gold': -0.15},
    ]


def test_operator():
    session = Session()
    post = Post(PID, session=session)
    same_post = Post(PID, session=session)
    another_post = Post(138966430, session=session)
    assert post == same_post
    assert post != another_post
    assert post > another_post
    assert post >= another_post
    assert post >= same_post
    assert another_post < post
    assert another_post <= post
    assert post <= same_post


def test_attachments():
    session = Session()
    post = Post(PID, session=session)
    assert post.attachments == []
    post = Post(283846735, session=session)
    assert post.attachments == [
        {
            'attachurl': 'mon_201807/01/-7knvQ5-dk0pX11ZaeT3cS1hn-1hn.jpg',
            'size': 3745,
            'type': 'img',
            'subid': 0,
            'url_utf8_org_name': '',
            'dscp': '',
            'path': 'mon_201807/01',
            'name': '-7knvQ5-dk0pX11ZaeT3cS1hn-1hn.jpg',
            'ext': 'jpg',
            'thumb': 120
        },
        {
            'attachurl': 'mon_201807/01/-7knvQ5-ci95XdZ3iT3cSqo-zk.jpg',
            'size': 1261,
            'type': 'img',
            'subid': 1,
            'url_utf8_org_name': '',
            'dscp': '',
            'path': 'mon_201807/01',
            'name': '-7knvQ5-ci95XdZ3iT3cSqo-zk.jpg',
            'ext': 'jpg',
            'thumb': 120
        }
    ]
