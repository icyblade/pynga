from pynga import NGA
from pynga.post import Post

UID = -1
CID = ''


def parse(tid):
    nga = NGA()
    thread = nga.Thread(tid)
    for lou, post in thread.posts.items():
        yield post.user.uid


def main():
    tid = 12496011
    nga = NGA({'uid': UID, 'cid': CID})
    thread = nga.Thread(tid)
    for lou, post in thread.posts.items():
        if isinstance(post, Post) and post.pid is not None:
            response = post.add_point(600, 'test', '给作者发送PM')
            message = response['data']['0']
            if message != '操作成功':
                print(f'{post} failed, message: {message}')


if __name__ == '__main__':
    main()
