#! coding: utf8
"""群体扣分"""

import sys, glob, os
from datetime import datetime, timedelta
from multiprocessing import Process, current_process, cpu_count
from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker
from config.authentication import login_uid, login_cid
from NGA import NGA
from lib.useful_functions import timestamp2str, split

def examine(chunk, login_uid, login_cid):
    fo = open('result/cheat_wardens_%s.icy.txt' % current_process().name, 'w')
    nga = NGA(login_uid, login_cid)
    pbar = ProgressBar(widgets=['Running: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' '], maxval=len(chunk)).start()
    counter = 0
    
    for uid, fids in chunk:
        pbar.update(counter)
        counter += 1
        return_str = ''
        u = nga.User(uid)
        return_str += '---------- FID: %s, UID: %s, Username: %s ------------\n' % (','.join(map(str, fids)), uid, u.username)
        
        # get logs
        original_logs = u.get_admin_log_done(datetime.now()-timedelta(1))
        
        # count logs
        cnt, dup = {}, {}
        for log in original_logs:
            k = (log['type'], log['target_uid'], log['target_tid'], log['target_pid'])
            v = (log['description'], log['timestamp'])
            if k in cnt:
                cnt[k].append(v)
            else:
                cnt[k] = [v]
        
        # find duplication
        for k, v in cnt.iteritems():
            if len(v) != 1 and nga.Thread(k[2]).get_fid() in fids:
                dup[k] = v
                
        # output
        if dup:
            for k, v in dup.iteritems():
                return_str += 'Type %s, UID: %s, TID: %s, PID: %s, Done %s times. Infos:\n' % (
                    k[0], k[1], k[2], k[3], len(v[0])
                )
                for description, timestamp in v:
                    return_str += '%s %s\n' % (description, timestamp2str(timestamp))
                return_str += '\n'
        else:
            return_str += 'Good!\n\n'
        fo.write(return_str.encode(sys.getfilesystemencoding(), 'ignore'))
    fo.close()
    pbar.finish()
    
def main():
    target_tid = 9055671 # 目标 TID
    nga = NGA(login_uid, login_cid)
    t = nga.Thread(target_tid)
    replies = t.get_replies()
    
    # split
    chunks = split(wardens_data, [1]*(cpu_count()))
    
    # output dir check
    if not os.path.exists('./result/'):
        os.mkdir('./result/')
    
    # deliver jobs
    processes = []
    for chunk in chunks:
        p = Process(target=examine, args=(chunk, login_uid, login_cid))
        p.start()
        processes.append(p)
    for process in processes: process.join()
    
    # merge data
    data = ''
    for file in glob.glob('result/cheat_wardens_*.icy.txt'):
        with open(file, 'r') as f:
            data += f.read()
        os.remove(file)
    with open('result/cheat_wardens.txt', 'w') as f:
        f.write(data)
    f.close()
    
if __name__ == '__main__':
    main()
