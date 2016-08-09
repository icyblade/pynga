import urllib, urllib2, socket, chardet, json
from logger import configure_logger

class ParallelUrllib:
    def __init__(self, retry=50, timeout=30):
        #self.opener = urllib2.build_opener(urllib2.ProxyHandler({'http': '127.0.0.1:8080'}))
        self.opener = urllib2.build_opener()
        self.retry = retry
        self.timeout = timeout
        self.logger = configure_logger(__name__)
        
    def close(self):
        self.opener.close()
        
    def __del__(self):
        self.close()
        
    def addheaders(self, d):
        self.opener.addheaders = d
        
    def set_header(self, key, value):
        for idx, cont in enumerate(self.header):
            if cont[0] == key:
                self.header[idx] = (key, value)
            else:
                self.header.append((key, value))
        
    def get_json(self, url):
        return self.html2json(self.get(url))
            
    def post_json(self, url, data):
        return self.html2json(self.post(url, data))
            
    def get(self, url):
        tries, html = 1, None
        while tries <= self.retry and not isinstance(html, str) and not isinstance(html, unicode):
            html = self.get_once(url)
            tries += 1
        return html
        
    def post(self, url, data):
        tries, html = 1, None
        while tries <= self.retry and not isinstance(html, str) and not isinstance(html, unicode):
            html = self.post_once(url, data)
            tries += 1
        return html 
        
    def get_once(self, url):
        try:
            self.logger.debug('Getting %s' % url)
            r = self.opener.open(url, timeout = self.timeout)
            html = r.read()
        except (urllib2.HTTPError, urllib2.URLError, socket.error, socket.timeout) as e:
            return e
        return self.decode(html)

    def post_once(self, url, data):
        """
        ptype data: dict
        """
        try:
            self.logger.debug('Posting %s with data %s' % (url, data))
            r = self.opener.open(url, urllib.urlencode(data), timeout = self.timeout)
            html = r.read()
        except (urllib2.HTTPError, urllib2.URLError, socket.error, socket.timeout) as e:
            return e
        return self.decode(html)
        
    def html2json(self, html):
        if html.startswith('window.script_muti_get_var_store='):
            return json.loads(html[33:], strict=False) # 33 = length of 'window.script_muti_get_var_store='
        else:
            return json.loads(html, strict=False)

    def decode(self, html):
        """
        charset = chardet.detect(html)
        self.logger.debug('Charset: %s' % charset)
        html = html.decode(charset['encoding'], 'ignore')
        """
        html = html.decode('gbk', 'ignore')
        return html
        