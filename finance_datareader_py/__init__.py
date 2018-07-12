# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import numpy as np
import pandas.compat as compat
import requests
from pandas.compat import StringIO, bytes_to_str
from pandas_datareader.base import _DailyBaseReader

from ._version import get_versions

__all__ = ['netease', 'sohu', 'sse', 'szse', 'gtimg', 'eastmoney', 'xueqiu']

__version__ = get_versions()['version']
del get_versions


class _AbsDailyReader(_DailyBaseReader):
    """每日汇总数据基类

    封装了_get_response。默认提供仿浏览器浏览的headers
    """
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '66.0.3359.181 Safari/537.36'}

    def __init__(self, symbols=None, start=None, end=None, retry_count=3,
                 pause=0.001, session=None, chunksize=25):

        super(_AbsDailyReader, self).__init__(symbols, start, end,
                                              retry_count, pause, session,
                                              chunksize)
        self._encoding = 'utf-8'
        # _read_url_as_StringIO中待解析内容长度小于
        # self._read_url_as_StringIO_min_len时是否抛出异常
        self._read_url_as_StringIO_less_min_len = False
        # _read_url_as_StringIO中待解析内容长度有效最小长度，小于此长度被认为无效
        self._read_url_as_StringIO_min_len = 0

    def _get_response(self, url, params=None, headers=None):
        if not headers:
            headers = _AbsDailyReader._headers
        return super(_AbsDailyReader, self)._get_response(url, params, headers)

    def _get_cookie(self, url, headers=None):
        if not headers:
            headers = _AbsDailyReader._headers
        return requests.get(url, headers=headers).cookies

    def _convert_numeric(self, df, columns, errors='ignore', copy=False):
        """转换DataFrame中的指定列为 ``np.float64`` 类型"""
        for col in columns:
            df[col] = df[col].astype(np.float64, errors=errors, copy=copy)
        return df

    def _convert_numeric_allcolumns(self, df, errors='ignore', copy=False):
        """转换整个DataFrame中的所有列数据类型为 ``np.float64`` """
        return self._convert_numeric(df, df.columns, errors=errors, copy=copy)

    def _read_url_as_StringIO(self, url, params=None, min=0, errors='ignore'):
        """重写基类同名方法

        根据派生类提供的encoding解析文本
        """
        response = self._get_response(url, params=params)
        text = self._sanitize_response(response)
        out = StringIO()
        if len(text) <= self._read_url_as_StringIO_min_len:
            if self._read_url_as_StringIO_less_min_len:
                service = self.__class__.__name__
                raise IOError("{} request returned no data; check URL for "
                              "invalid inputs: {}".format(service, self.url))
            else:
                return None
        if isinstance(text, compat.binary_type):
            out.write(bytes_to_str(text, encoding=self._encoding))
        else:
            out.write(text)
        out.seek(0)
        return out
