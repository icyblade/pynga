#! coding: utf8
import threading, datetime
from NGA import NGA
from config.authentication import login_uid, login_cid
from itertools import count
from operator import itemgetter
from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker
from threading import Thread

nga = NGA(login_uid, login_cid)

def main():
    legion_fid = 476

    f = nga.Forum(legion_fid)
    posts = list(f.get_all_posts())
    i = count(1)
    
    db = {}
    pbar = ProgressBar(widgets=['Running: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' '], maxval=len(posts)).start()
    for idx, tid in enumerate(posts):
        pbar.update(idx)
        t = nga.Thread(tid)
        author_name, points = t.get_point()
        if not author_name is None:
            if author_name in db:
                db[author_name][tid] = points
            else:
                db[author_name] = {
                    tid: points,
                }
    pbar.finish()

    database = {
        'Warden': [],
        'Folk': [],
    }
    for uid, data in db.iteritems():
        try:
            u = nga.User(uid)
            if u.group in ['Warden', 'Scythe', 'Titan', 'Arbiter']:
                database['Warden'].append((u.username, sum([sum(i) for i in data.values()])))
            else:
                database['Folk'].append((u.username, sum([sum(i) for i in data.values()])))
        except UnicodeEncodeError:
            database['Folk'].append((u.username, sum([sum(i) for i in data.values()])))
            print(username)
    database = dict([(k, sorted(v, key=itemgetter(1), reverse=True)) for k, v in database.iteritems()])
    
    print('Last update: %s' % datetime.datetime.now())
    print('[table]')
    print(u'[tr][td]排名[/td][td]版主[/td][td]非版主[/td][/tr]')
    for i in xrange(20):
        print('[tr][td]%s[/td][td]%s[/td][td]%s[/td][/tr]' % (
            i+1,
            '%s %s' % database['Warden'][i],
            '%s %s' % database['Folk'][i],
        ))
    print('[/table]')

if __name__ == '__main__':
    main()
