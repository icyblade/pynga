#! coding: utf8
"""筛选刷操作量的版主"""

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

def load_wardens_data(nga, sub=True):
    # 载入版主数据
    batchs = []
    fids = nga.get_all_fids()
    for fid in fids:
        forum = nga.Forum(fid)
        uids = forum.get_wardens(sub=True)
        for uid in uids:
            batchs.append((fid, uid))
    
    # convert
    target_coeffs = {}
    for fid, uid in batchs:
        if uid in target_coeffs:
            target_coeffs[uid].append(fid)
        else:
            target_coeffs[uid] = [fid]
            
    # check if uid is warden
    for uid in target_coeffs:
        u = nga.User(uid)
        if u.group == '4': # is warden
            target_coeffs.pop(uid, None)
            
    # create backup
    with open('data/wardens_data.txt', 'w') as f:
        for uid, fids in target_coeffs.iteritems():
            f.write('%s,%s\n' % (uid, ','.join(map(str, fids))))
    return target_coeffs.items()
    
def main():
    nga = NGA(login_uid, login_cid)
    wardens_data = load_wardens_data(nga, sub=True)
    """
    with open('data/wardens_data.txt', 'r') as f:
        batchs = [l.split(',') for l in f.read().splitlines()]
        wardens_data = [(i[0], i[1:]) for i in batchs]
    """
    
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
