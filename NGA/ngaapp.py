class NGAApp:
    """App 实现"""
    def __init__(self, uid):
        """
        :param uid: 用户 ID
        """
        self.uid = uid
        self.nga_client_checksum = ''
        self.app_id = 1010
        self.access_token = ''
        self.t = 
        self.sign = ''
        self.user_agent = 'Nga_Official/574(iPhone 2333HQ;icyOS 2.3.3)'
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-Agent', self.user_agent)]
        
    def get_quests(self):
        """获取日常任务列表"""
        url = 'http://bbs.ngacn.cc/app_api.php?__lib=checkin&__act=detail&__ngaClientChecksum=%s' % self.nga_client_checksum
        post_data = urllib.urlencode({
            'app_id': self.app_id,
            'access_uid': self.uid,
            'access_token': self.access_token,
            't': self.t,
            'sign': self.sign,
            'send_ua': '',
            'mver': 2,
            'fid': 0,
        })
        r = self.opener.open(url, post_data)
        html = r.read()
        json_data = json.loads(html)
        
        if json_data['code'] == 0:
            for i in json_data['result']['missions']['available']:
                yield i
        else:
            print('%s %s' % (json_data['code'], json_data['msg']))
            raise Exception(json_data['msg'])
            
    def get_sign(self, t):
        print(hashlib.md5('%s%s%s%s' % (
            str(self.app_id),
            self.access_token,
            str(t),
            '392e916a6d1d8b7523e2701470000c30bc2165a1'
        )).hexdigest())
        return hashlib.md5('%s%s%s%s' % (
            str(self.app_id),
            self.access_token,
            str(t),
            '392e916a6d1d8b7523e2701470000c30bc2165a1'
        )).hexdigest()
            
    def checkin(self, id):
        """做某日常任务
        :param id: 任务 ID
        """
        url = 'http://bbs.ngacn.cc/app_api.php?__lib=checkin&__act=dosign&__ngaClientChecksum=%s' % self.nga_client_checksum
        post_data = urllib.urlencode({
            'app_id': self.app_id,
            'access_uid': self.uid,
            'access_token': self.access_token,
            't': self.t,
            'sign': self.sign,
            'send_ua': '',
            'mid': id,
            'checkin': 1,
            'event': 1,
        })
        r = self.opener.open(url, post_data)
        html = r.read()
        json_data = json.loads(html)
        return json_data['msg']

