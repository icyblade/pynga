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
        """获取某页的所有 PID（不包含楼主和贴条）
        rtype: PID, timestamp, UID, 楼层, 内容, 附件(没有是 None)
        """
        url = 'http://bbs.ngacn.cc/read.php?tid={self.tid}&lite=js&page={page}'.format(
            self = self, page = page
        )
        json_data = self.opener.get_json(url)
        for k, reply in json_data['data']['__R'].iteritems():
            lou = int(reply['lou'])
            if lou != 0: # 排除楼主
                if 'pid' in reply:
                    # 正常回复
                    if 'attachs' in reply:
                        yield int(reply['pid']), int(reply['postdatetimestamp']), int(reply['authorid']), lou, reply['content'], reply['attachs']
                    else:
                        yield int(reply['pid']), int(reply['postdatetimestamp']), int(reply['authorid']), lou, reply['content'], None
                elif 'comment_to_id' in reply:
                    # 贴条
                    pass
                    
        
    def get_replies(self):
        """获取本贴所有 PID（不包含楼主和贴条）
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

    def get_point(self):
        """获取主楼加分信息
        rvalue: (uid, [float(声望),float(威望),float(金币)])
        """
        json_data = self.opener.get_json('http://bbs.ngacn.cc/read.php?tid={self.tid}&lite=js'.format(self=self))
        author_id = json_data['data']['__T']['authorid']
        try:
            info = re.findall(
                '\[[U]?([0-9.\-]+) ([0-9.\-]+) ([0-9.\-]+)[^\]]*\]\([\S\s]+?\)',
                json_data['data']['__R']['0']['alterinfo']
            ) # old pattern
            info1 = re.findall('\[[AU]?([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+) [^\]]*\]', json_data['data']['__R']['0']['alterinfo'])
            info = info + info1
        except KeyError:
            return (None, [[0, 0, 0]])
        return (author_id, [map(float, i) for i in info])
