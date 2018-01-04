from pynga.default_config import FORUM_PAGE_SLOW_QUERY_LIMIT, HOST
from pynga.thread import Thread


class Forum(object):
    def __init__(self, fid, session=None, page_limit=20):
        self.fid = fid
        self.page_limit = page_limit
        if page_limit > FORUM_PAGE_SLOW_QUERY_LIMIT:
            raise NotImplementedError('Slow query is now supported yet.')
        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')

    def __repr__(self):
        return f'<pynga.forum.Forum, fid={self.fid}>'

    @property
    def raw(self):
        from math import ceil

        raw_all = {}
        page = 1
        while True:
            raw = self.session.get_json(
                f'{HOST}/thread.php?fid={self.fid}&lite=js&page={page}&order_by=postdatedesc&nounion=1'
            )
            raw_all[page] = raw
            n_pages = ceil(raw['data']['__ROWS'] / raw['data']['__T__ROWS_PAGE'])
            if page < n_pages and page < self.page_limit:
                page += 1
            else:
                break

        return raw_all

    @property
    def threads(self):
        from collections import OrderedDict

        threads = OrderedDict([])
        for page, raw in self.raw.items():
            # process threads
            for _, thread_raw in raw['data']['__T'].items():
                threads[thread_raw['tid']] = Thread(thread_raw['tid'], session=self.session)

        return threads
