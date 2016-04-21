#! coding: utf8
import json, time, re, sys
from operator import itemgetter
from datetime import datetime, timedelta
from lib.parallel_urllib import ParallelUrllib

class Post:
    def __init__(self, pid, opener):
        self.pid = pid
        self.opener = opener
    
    def get_comments(self):
        """获取本 PID 的所有贴条
        rtype: pid, timestamp, uid
        """
        url = 'http://bbs.ngacn.cc/read.php?pid={self.pid}&lite=js'.format(
            self = self
        )
        json_data = self.opener.get_json(url)
        if 'comment' in json_data['data']['__R']['0']:
            for k, content in json_data['data']['__R']['0']['comment']:
                yield int(content['pid']), int(content['postdatetimestamp']), int(content['authorid'])
        else:
            yield 0, 0, 0

    def add_point(self, value, info, tid, pm=True, addmoney=True, norvrc=False):
        """加分"""
        url = 'http://bbs.ngacn.cc/nuke.php?func=addpoint&tid={tid}&pid={self.pid}'.format(
            self = self, tid = tid
        )
        post_data = {
            'rcvc': value,
            'info': info,
            'pm'  : 1 if pm else 0,
            'addmoney': 1 if addmoney else 0,
            'norvrc': 1 if norvrc else 0,
        }
        #sys.stdout.write(str(url)+'\n')
        self.opener.post_once(url, post_data) # todo post 会重复加分，solve it
            