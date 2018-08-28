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


def test_multiple_workers():
    from time import time

    test_fids = [
        7, 8, 10, 102, 102, 116, 124, 124, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
        191, 200, 201, 213, 218, 230, 240, 254, 255, 264, 264, 272, 306, 310, 310, 318, 320,
        321, 323, 332, 334, 335, 353, 388, 390, 406, 411, 412, 414, 414, 416, 420, 422, 424,
        425, 426, 427, 428, 431, 431, 433, 434, 435, 436, 436, 441, 442, 443, 444, 445, 447,
        452, 453, 454, 455, 459, 463, 465, 466, 468, 469, 472, 472, 474, 476, 477, 480, 481,
        482, 484, 486, 487
    ]
    max_workers = 5

    # one worker
    start = time()
    result = []
    nga = NGA(AUTHENTICATION, max_workers=1)
    for i in test_fids:
        result.append(nga.Forum(i, page_limit=1))
    end = time()
    single_time = end - start

    # multiple workers
    with pytest.raises(NotImplementedError):
        start = time()
        result = []
        nga = NGA(AUTHENTICATION, max_workers=5)
        for i in test_fids:
            result.append(nga.Forum(i, page_limit=1))
        end = time()
        multi_time = end - start
    multi_time = 0

    print(f'{max_workers} threads: {multi_time:.2f}, 1 thread: {single_time:.2f}')

    assert multi_time <= single_time / 3
