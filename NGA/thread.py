#! coding: utf8
import json, time, re
from operator import itemgetter
from datetime import datetime, timedelta
from lib.parallel_urllib import ParallelUrllib
from post import Post

class Thread:
    def __init__(self, tid, opener):
        self.tid = tid
        self.opener = opener
        
    def Post(self, pid):
        return Post(pid, self.opener)
    
    def get_fid(self):
        """获取帖子所在板块 ID"""
        url = 'http://bbs.ngacn.cc/read.php?tid={self.tid}&lite=js'.format(
            self = self
        )
        html = self.opener.get(url)
        try:
            return int(re.findall('"__T":{"fid":[0-9]+', html)[0][13:]) # faster than json.loads
        except IndexError:
            return 0

    def get_replies_in_page(self, page):
        """获取某页的所有 PID（不包含楼主）
        rtype: PID, timestamp, UID, 楼层
        """
        url = 'http://bbs.ngacn.cc/read.php?tid={self.tid}&lite=js&page={page}'.format(
            self = self, page = page
        )
        json_data = self.opener.get_json(url)
        for k, reply in json_data['data']['__R'].iteritems():
            lou = reply['lou']
            if reply['lou'] != 0:
                if 'pid' in reply:
                    # 正常回复
                    yield int(reply['pid']), int(reply['postdatetimestamp']), int(reply['authorid']), int(reply['lou'])
                elif 'comment_to_id' in reply:
                    # 贴条
                    p = self.Post(json_data['data']['__R']['0']['comment_to_id'])
                    for pid, timestamp, uid, lou in p.get_comments():
                        # TODO: 等二哥修 biug
                        pass
                    
        
    def get_replies(self):
        """获取本贴所有 PID
        rtype: PID, timestamp, UID, 楼层
        """
        url = 'http://bbs.ngacn.cc/read.php?tid={self.tid}&lite=js'.format(
            self = self
        )
        json_data = self.opener.get_json(url)
        total_replies = json_data['data']['__T']['replies']
        total_pages = int(total_replies/20)+1
        for page in xrange(1, total_pages+1):
            for i in self.get_replies_in_page(page):
                yield i
