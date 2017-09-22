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
    assert post.user.uid == None
    assert post.user.username == None

def test_subject():
    session = Session()
    post = Post(PID, session=session)
    assert post.subject == 'test'

    post = Post(session=session)
    assert post.subject == None

def test_content():
    session = Session()
    post = Post(PID, session=session)
    assert post.content == '占楼占楼占楼占楼占楼占楼占楼占楼<br/>备用楼'

    post = Post(session=session)
    assert post.content == None