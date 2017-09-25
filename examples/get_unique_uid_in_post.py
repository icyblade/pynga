from pynga import NGA


def parse(tid):
    nga = NGA()
    thread = nga.Thread(tid)
    for lou, post in thread.posts.items():
        yield post.user.uid


def main():
    tid = 11868989
    unique_uid = sorted(list(set(parse(tid))))
    print(unique_uid)


if __name__ == '__main__':
    main()
