from time import time

from pynga import NGA
from . import local


@local
def test_stress():
    TID = 13405313  # 1128 pages

    start = time()
    nga = NGA()
    thread = nga.Thread(TID, page_limit=100)  # 100 requests
    for lou, post in thread.posts.items():  # 1999 floors, 2000 iterations
        assert post.user.uid is None or post.user.uid > 0  # 1 request
    end = time()

    """There are 100+2000=2100 requests to be made(without optimization).
    I hope we can do this in 60 seconds.
    """
    print(f'{__name__} duration: {end-start:.2f}s')


@local
def test_object_reuse():
    nga = NGA()

    one = nga.Thread(13405313, page_limit=1)
    other = nga.Thread(13405313, page_limit=1)
    assert id(one) == id(other)

    one = nga.User(uid=58)
    other = nga.User(uid=58)
    assert id(one) == id(other)

    one = nga.Post(267645659)
    other = nga.Post(267645659)
    assert id(one) == id(other)

    one = nga.Forum(7)
    other = nga.Forum(7)
    assert id(one) == id(other)
