#! coding: utf8

import re

class Forum:
    def __init__(self, fid, opener):
        self.fid = fid
        self.opener = opener
        
    def get_wardens(self, sub=False):
        """
        param sub: 只返回副版主
        """
        url = 'http://bbs.ngacn.cc/nuke.php?__lib=view_privilege&__act=view&fid={self.fid}&__output=8'.format(self=self)
        data = self.opener.get_json(url)['data']['0']
        if sub:
            idx = data.find(u'<h4 class=til>副版主</h4>')
            data = data[idx:]
        wardens = re.findall(r"nuke.php\?func=ucp\&uid=[0-9]+'>[\S]+</a>", data)
        for i in wardens:
            yield int(re.findall('uid=[0-9]+', i)[0][4:])
            
    def get_all_posts(self):
        """
        rvalue: yield 所有 tid，包括镜像
        """
        url_template = 'http://bbs.ngacn.cc/thread.php?fid={self.fid}&lite=js&page={page}'
        page = 1
        while True:
            json_data = self.opener.get_json(url_template.format(
                self = self,
                page = page,
            ))
            if len(json_data['data']['__T']) == 0:
                break
            for idx, element in json_data['data']['__T'].iteritems():
                if element['quote_from'] != 0:
                    yield int(element['quote_from'])
                yield int(element['tid'])
            page += 1
        
