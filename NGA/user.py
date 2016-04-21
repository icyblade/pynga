#! coding: utf8
import json, time, re
from datetime import datetime, timedelta
from operator import itemgetter
from lib.parallel_urllib import ParallelUrllib

class User:
    def __init__(self, uid, opener):
        self.uid = uid
        self.opener = opener
        self.get_user_info()
        
    def get_user_info(self):
        """获取本用户信息"""
        url = 'http://bbs.ngacn.cc/nuke.php?__lib=ucp&__act=get&uid={self.uid}&lite=js'.format(
            self = self,
        )
        self.user_info = self.opener.get_json(url)
        self.username = self.user_info['data']['0']['username']
        self.group = self.user_info['data']['0']['group']
        
    def get_admin_log_done(self, start_datetime=None):
        """获取操作记录
        ptype start_datetime: datetime.datetime
        """
        if not start_datetime:
            start_datetime = datetime.now() - timedelta(1)
        page = 1
        logs = []
        start_timestamp = time.mktime(start_datetime.timetuple())
        while True:
            url = 'http://bbs.ngacn.cc/nuke.php?__lib=admin_log_search&__act=search&from={self.uid}&__output=8'.format(self = self)
            post_data = {
                'page': page,
            }
            json_data = self.opener.post_json(url, post_data)
            if json_data['data']['0'] == {}:
                return logs
            for k, v in sorted(json_data['data']['0'].items(), key=itemgetter(0)):
                id, typ, source_uid, target_uid, target_tid, description, timestamp = v['0'], v['1'], v['2'], v['3'], v['4'], v['5'], v['6']
                pids = re.findall('\[PID:[0-9]+\]', description)
                if pids:
                    target_pid = pids[0][5:-1]
                else:
                    target_pid = 0
                if timestamp < start_timestamp:
                    return logs
                logs.append({
                    'id': int(id),
                    'type': json_data['data']['2'][str(typ)],
                    'source_uid': int(source_uid),
                    'target_uid': int(target_uid),
                    'target_tid': int(target_tid),
                    'target_pid': int(target_pid),
                    'description': description,
                    'timestamp': int(timestamp),
                })
            page += 1
            
    def undo_admin(self, log_id):
        """取消操作 experimental"""
        url = 'http://bbs.ngacn.cc/nuke.php?__lib=undo&__act=undo&raw=3&logid={log_id}'.format(log_id=log_id)
        post_data = {
            'nouse': 'post',
        }
        self.opener.post(url, post_data)
