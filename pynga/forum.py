from pynga.default_config import FORUM_PAGE_SLOW_QUERY_LIMIT, HOST
from pynga.thread import Thread


class Forum(object):
    """NGA 版面基础类.

    Parameters
    --------
    fid: int
        版面 FID.
    session: :class:`Session <pynga.session.Session>`
        获取数据所使用的 session.
    page_limit: int
        最大页面数量. 默认: 20.

    Attributes
    --------
    page_limit: int
        最大页面数量.
    """
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
    def _raw(self):
        """原始 JSON 数据."""
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
        """获取当前版面的帖子, 按照发帖时间降序排列.

        Returns
        --------
        OrderedDict(tid, :class:`Thread <pynga.thread.Thread>`)
            当前版面的帖子. 最多不超过 :attr:`page_limit <pynga.forum.Forum.page_limit>`.
        """
        from collections import OrderedDict

        threads = OrderedDict([])
        for page, raw in self._raw.items():
            # process threads
            for _, thread_raw in raw['data']['__T'].items():
                if 'quote_from' in thread_raw and thread_raw['quote_from']:
                    threads[thread_raw['quote_from']] = Thread(thread_raw['quote_from'], session=self.session)
                else:
                    threads[thread_raw['tid']] = Thread(thread_raw['tid'], session=self.session)

        return threads


class SubForum(object):
    """NGA 合集基础类.

    Parameters
    --------
    fid: int
        版面 FID.
    session: :class:`Session <pynga.session.Session>`
        获取数据所使用的 session.
    page_limit: int
        最大页面数量. 默认: 20.

    Attributes
    --------
    page_limit: int
        最大页面数量.
    """
    def __init__(self, stid, session=None, page_limit=20):
        self.stid = stid
        self.page_limit = page_limit
        if page_limit > FORUM_PAGE_SLOW_QUERY_LIMIT:
            raise NotImplementedError('Slow query is now supported yet.')
        if session is not None:
            self.session = session
        else:
            raise ValueError('session should be specified.')

    def __repr__(self):
        return f'<pynga.forum.SubForum, stid={self.stid}>'

    @property
    def _raw(self):
        """原始 JSON 数据."""
        from math import ceil

        raw_all = {}
        page = 1
        while True:
            raw = self.session.get_json(
                f'{HOST}/thread.php?stid={self.stid}&lite=js&page={page}&order_by=postdatedesc&nounion=1'
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
        """获取当前合集的帖子, 按照发帖时间降序排列.

        Returns
        --------
        OrderedDict(tid, :class:`Thread <pynga.thread.Thread>`)
            当前版面的帖子. 最多不超过 :attr:`page_limit <pynga.forum.SubForum.page_limit>`.
        """
        from collections import OrderedDict

        threads = OrderedDict([])
        for page, raw in self._raw.items():
            # process threads
            for _, thread_raw in raw['data']['__T'].items():
                threads[thread_raw['tid']] = Thread(thread_raw['tid'], session=self.session)

        return threads
