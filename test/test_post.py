import pytest

from pynga.post import Post
from pynga.session import Session

PID = 138966442


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
    session = Session()
    post = Post(PID, session=session)
    assert post.user.username == 'icyblade'

    post = Post(session=session)
    assert post.user.uid is None
    assert post.user.username is None


def test_subject():
    session = Session()
    post = Post(PID, session=session)
    assert post.subject == 'test'

    post = Post(session=session)
    assert post.subject is None


def test_content():
    session = Session()
    post = Post(PID, session=session)
    assert post.content == '占楼占楼占楼占楼占楼占楼占楼占楼<br/>备用楼'

    post = Post(session=session)
    assert post.content is None


def test_tid():
    session = Session()
    post = Post(PID, session=session)
    assert post.tid == 7384678


def test_fid():
    session = Session()
    post = Post(PID, session=session)
    assert post.fid == 188


def test_alterinfo():
    session = Session()
    post = Post(PID, session=session)
    assert list(post.alterinfo) == [
        {'action': 'E', 'edit_timestamp': 1506041993},
        {'action': 'A', 'reputation': 15, 'prestige': 0.1, 'gold': 0.15, 'action_id': 12258940, 'info': ''},
        {'action': 'U', 'reputation': -15, 'prestige': -0.1, 'gold': -0.15},
        {'action': 'A', 'reputation': 15, 'prestige': 0.1, 'gold': 0.15, 'action_id': 12258960, 'info': 'pynga_test'},
        {'action': 'U', 'reputation': -15, 'prestige': -0.1, 'gold': -0.15},
    ]
