#! coding: utf8
"""NGA 各项功能的 Python 实现"""

import urllib, urllib2, re, json, time, hashlib
from bs4 import BeautifulSoup
from datetime import date
from config import USER_AGENT
from forum import Forum
from lib.parallel_urllib import ParallelUrllib
from thread import Thread
from user import User
from post import Post

class NGA:
    """Web 端实现"""
    def __init__(self, uid, cid):
        """
        :param uid: 用户 ID
        :param cid: 浏览器 Cookie 的 ngaPassportCid 的值
        """
        self.opener = ParallelUrllib()
        self.login_uid = uid
        self.login_cid = cid
        self.opener.addheaders([
            ('Cookie', 'ngaPassportUid={uid}; ngaPassportCid={cid};'.format(
                uid = uid,
                cid = cid,
            )),
            ('User-Agent', USER_AGENT),
        ])
        self.get_login_user_info()
        
    def __del__(self):
        self.opener.close()
        
    def User(self, uid):
        return User(uid, self.opener)
        
    def Forum(self, fid):
        return Forum(fid, self.opener)
        
    def Thread(self, tid):
        return Thread(tid, self.opener)
        
    def Post(self, pid):
        return Post(pid, self.opener)
        
    def get_all_fids(self):
        """获取所有公开版面列表
        rtype: list of str
        """
        html = self.opener.get(
            'http://bbs.ngacn.cc/template/js/nga_index_forums.xml'
        )
        return list(set([
            int(i[5:-1])
            for i in re.findall('fid=\'[-]?[0-9]+\'',html)
        ]))
        
    def get_login_user_info(self):
        """获取登陆用户信息"""
        self.login_user = User(self.login_uid, self.opener)
