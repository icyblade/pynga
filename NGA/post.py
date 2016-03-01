#! coding: utf8
import json, time, re
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
