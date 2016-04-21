#! coding: utf8
"""群体加分"""

import sys, glob, os, re
from datetime import datetime, timedelta
from multiprocessing import Process, current_process, cpu_count
from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker
from config.authentication import login_uid, login_cid
from NGA import NGA
from lib.useful_functions import timestamp2str, split

def add_them(chunk, login_uid, login_cid, target_tid):
    nga = NGA(login_uid, login_cid)
    pbar = ProgressBar(widgets=['Running: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' '], maxval=len(chunk)).start()
    counter = 0
    
    for uid, pid in chunk:
        pbar.update(counter)
        counter += 1
        post = nga.Post(pid)
        post.add_point('lv01', '', target_tid, pm=True, addmoney=True, norvrc=True)
    pbar.finish()
    
def main():
    target_tid = 0 # 目标 TID
    nga = NGA(login_uid, login_cid)
    t = nga.Thread(target_tid)
    replies = t.get_replies()
    dataset = {}
    for pid, timestamp, uid, lou, content, attachs in replies:
        if (re.findall('\[img\][\S]+\[/img\]', content) or attachs) and uid>0:
            dataset[uid] = pid
    dataset = [(uid, pid) for uid, pid in dataset.iteritems()]
    
    pbar = ProgressBar(widgets=['Running: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' '], maxval=len(dataset)).start()
    counter = 0
    
    for uid, pid in dataset:
        pbar.update(counter)
        counter += 1
        post = nga.Post(pid)
        post.add_point('lv01', '', target_tid, pm=True, addmoney=False, norvrc=True)
    pbar.finish()
    """
    # split
    chunks = split(dataset, [1]*(cpu_count()))
    
    # deliver jobs
    processes = []
    for chunk in chunks:
        p = Process(target=add_them, args=(chunk, login_uid, login_cid, target_tid))
        p.start()
        processes.append(p)
    for process in processes: process.join()
    """

    
if __name__ == '__main__':
    main()
