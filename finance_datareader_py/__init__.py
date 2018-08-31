# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import datetime

import numpy as np
import pandas as pd
import pandas.compat as compat
import requests
from pandas.compat import StringIO, bytes_to_str
from pandas_datareader.base import _DailyBaseReader

from ._version import get_versions

__all__ = ['netease', 'sohu', 'sse', 'szse', 'gtimg', 'eastmoney', 'xueqiu',
           'csrc', 'csindex', 'hexun', 'sina', 'DailyReader']

__version__ = get_versions()['version']
del get_versions


def _random(n=13):
    from random import randint
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(randint(start, end))


class _AbsDailyReader(_DailyBaseReader):
    """每日汇总数据基类

    封装了_get_response。默认提供仿浏览器浏览的headers
    """

    @staticmethod
    def _default_headers():
        return {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                              '10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome 66.0.3359.181 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7', }

    def _init_headers(self):
        self._headers = _AbsDailyReader._default_headers()

    def _append_header(self, name, value):
        """将指定的值加入到 _headers 中"""
        self._headers[name] = value

    def __init__(self, symbols=None, start=None, end=None, retry_count=3,
                 pause=1, session=None, chunksize=25):

        super(_AbsDailyReader, self).__init__(symbols, start, end,
                                              retry_count, pause, session,
                                              chunksize)
        self._encoding = 'utf-8'
        # _read_url_as_StringIO中待解析内容长度小于
        # self._read_url_as_StringIO_min_len时是否抛出异常
        self._read_url_as_StringIO_less_min_len = False
        # _read_url_as_StringIO中待解析内容长度有效最小长度，小于此长度被认为无效
        self._read_url_as_StringIO_min_len = 0
        self._init_headers()

    def _get_response(self, url, params=None, headers=None):
        if not headers:
            headers = _AbsDailyReader._default_headers()
        return super(_AbsDailyReader, self)._get_response(url, params, headers)

    def _get_cookie(self, url, headers=None):
        if not headers:
            headers = _AbsDailyReader._default_headers()
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


from finance_datareader_py.gtimg.daily import GtimgDailyReader  # noqa: E402


class DailyReader(_AbsDailyReader):
    """自动按照参数 ``zs_symbol`` 指定的基准代码（一般可以为指数代码）的每日成交
    汇总数据 附加 参数 ``symbols`` 指定的股票代码的每日成交汇总数据。
    并自动按照参数 ``fillna`` 的设定填充 :attr:`numpy.NaN` 数据。

    Args:
        symbols ({str, List[str],int, List[int]}):
            待查询的股票代码或集合。
        start (datetime.date): 开始日期。默认值：2004-10-08
        end (datetime.date): 结束日期。默认值：当前日期的 **前一天** 。
        retry_count (int): default 3
            Number of times to retry query request.
        pause (float): default 1
            Time, in seconds, of the pause between retries.
        session (Session): default None
            requests.sessions.Session instance to be used
        chunksize:
        sort_index (str): 数据按照索引的排序方式。默认值：asc
                * asc: 升序
                * desc: 降序
        fillna (str): 默认值：ffill
            参考 :meth:`pandas.DataFrame.fillna` 的参数 ``method``。
        reader (class): 读取数据使用的读取器。
            默认值：:class:`finance_datareader_py.gtimg.daily.GtimgDailyReader`
        type (str): 是否读取复权数据。默认值：None。
                * None: 不复权
                * 'qfq': 前复权
                * 'hfq': 后复权
        columns (List[str]): 从读取器 ``reader`` 中读取的列集合。默认值：['Close']
            *需要保证集合中的所有列均包含在读取器的返回列中*
        zs_symbol (str): 首先读取的基准代码（一般可以为指数代码）的编号。默认值：``sh000001``
            *此处根据业务需要，不一定需要传入指数代码*
        drop_zs_columns (bool): 是否在最终结果回传前丢弃从 ``zs_symbol`` 读取的相关列。默认值：True

    """

    def __init__(self, symbols, start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25, sort_index='asc', fillna='ffill',
                 reader=GtimgDailyReader, type=None, columns=['Close'],
                 zs_symbol='sh000001', drop_zs_columns=True):
        """自动按照参数 ``zs_symbol`` 指定的基准代码（一般可以为指数代码）的每日成交
        汇总数据 附加 参数 ``symbols`` 指定的股票代码的每日成交汇总数据。
        并自动按照参数 ``fillna`` 的设定填充 :attr:`numpy.NaN` 数据。

        Args:
            symbols ({str, List[str],int, List[int]}):
                待查询的股票代码或集合。
            start (datetime.date): 开始日期。默认值：2004-10-08
            end (datetime.date): 结束日期。默认值：当前日期的 **前一天** 。
            retry_count (int): default 3
                Number of times to retry query request.
            pause (float): default 1
                Time, in seconds, of the pause between retries.
            session (Session): default None
                requests.sessions.Session instance to be used
            chunksize:
            sort_index (str): 数据按照索引的排序方式。默认值：asc
                    * asc: 升序
                    * desc: 降序
            fillna (str): 默认值：ffill
                参考 :meth:`pandas.DataFrame.fillna` 的参数 ``method``。
            reader (class): 读取数据使用的读取器。
                默认值：:class:`finance_datareader_py.gtimg.daily.GtimgDailyReader`
            type (str): 是否读取复权数据。默认值：None。
                    * None: 不复权
                    * 'qfq': 前复权
                    * 'hfq': 后复权
            columns (List[str]): 从读取器 ``reader`` 中读取的列集合。默认值：['Close']
                *需要保证集合中的所有列均包含在读取器的返回列中*
            zs_symbol (str): 首先读取的基准代码（一般可以为指数代码）的编号。默认值：``sh000001``
                *此处根据业务需要，不一定需要传入指数代码*
            drop_zs_columns (bool): 是否在最终结果回传前丢弃从 ``zs_symbol`` 读取的相关列。默认值：True

        Returns (:class:`pandas.DataFrame`):


        Raises:
            ValueError: 当 ``symbols`` 或 ``reader`` 或 ``columns`` 或 ``zs_symbol`` 为
            ``None`` 时。

        """
        super(DailyReader, self).__init__(symbols=symbols, start=start, end=end,
                                          retry_count=retry_count, pause=pause,
                                          session=session, chunksize=chunksize)

        if not symbols:
            raise ValueError("'symbols' 不能为 None")
        if not reader:
            raise ValueError("'reader' 不能为 None")
        if not columns:
            raise ValueError("'columns' 不能为 None")
        if not zs_symbol:
            raise ValueError("'zs_symbol' 不能为 None")

        self._zs_symbol = zs_symbol
        self._reader_type = reader
        self._type = type
        self._sort_index = sort_index
        self._fillna = fillna
        self._columns = columns
        self._drop_zs_columns = drop_zs_columns

    def read(self) -> pd.DataFrame:
        """读取数据

        Returns (:class:`pandas.DataFrame`):
            无数据时返回空白的 :class:`pandas.DataFrame` 。
            参见 :attr:`pandas.DataFrame.empty`。

        Raises:
            RuntimeError: 当根据 `zs_symbol` 无法正确读取到数据时。

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py import DailyReader
                >>> df = DailyReader('601398').read()
                >>> print(df.tail())

                            Close
                Date
                2018-08-17   5.26
                2018-08-20   5.36
                2018-08-21   5.40
                2018-08-22   5.39
                2018-08-23   5.40

            .. code-block:: python

                >>> from finance_datareader_py import DailyReader
                >>> df = DailyReader(('601398', '601939', '601988')).read()
                >>> print(df.tail())

                            601398_Close  601939_Close  601988_Close
                Date
                2018-08-17          5.26          6.52          3.45
                2018-08-20          5.36          6.66          3.50
                2018-08-21          5.40          6.72          3.52
                2018-08-22          5.39          6.70          3.50
                2018-08-23          5.40          6.69          3.50

            .. code-block:: python

                >>> from finance_datareader_py import DailyReader
                >>> df = DailyReader(('601398', '601939'), columns=['Close', 'Open']).read()
                >>> print(df.tail())

                            601398_Close  601398_Open  601939_Close  601939_Open
                Date
                2018-08-17          5.26         5.30          6.52         6.65
                2018-08-20          5.36         5.29          6.66         6.55
                2018-08-21          5.40         5.38          6.72         6.65
                2018-08-22          5.39         5.40          6.70         6.71
                2018-08-23          5.40         5.38          6.69         6.70

            .. code-block:: python

                >>> from finance_datareader_py import DailyReader
                >>> df = DailyReader(601398, drop_zs_columns=False).read()
                >>> print(df.tail())

                            sh000001_Close  Close
                Date
                2018-08-17         2668.97   5.26
                2018-08-20         2698.47   5.36
                2018-08-21         2733.83   5.40
                2018-08-22         2714.61   5.39
                2018-08-23         2724.62   5.40
        """
        zs_reader = self._reader_type(symbols=self._zs_symbol, prefix='',
                                      suffix='',
                                      type=self._type, start=self.start,
                                      end=self.end,
                                      retry_count=self.retry_count,
                                      pause=self.pause, session=self.session,
                                      chunksize=self.chunksize)
        # 上证指数数据
        df = pd.DataFrame(zs_reader.read(), columns=self._columns)
        if df.empty:
            raise RuntimeError("没有找到关于指数 '{0}' 的相关数据。".format(self._zs_symbol))
            return df
        zs_reader.close()
        # 附加上证指数数据的列名前缀
        df = df.add_prefix(self._zs_symbol + '_')
        # 记录上证指数相关列名
        zs_columns = df.columns
        symbol_readers = self._create_readers()
        for symbol_reader in symbol_readers:
            # 循环读取单支股票的数据
            df_symbol = symbol_reader.read()
            if df_symbol.empty:
                continue
            df_symbol = df_symbol[self._columns]
            if len(symbol_readers) > 1:
                # 当待读取的股票数量 >1 时，自动在列名前增加前缀（股票代码_）
                df_symbol = df_symbol.add_prefix(symbol_reader.symbols + '_')
            symbol_reader.close()
            df = df.join(df_symbol)
        # 排序
        if self._sort_index:
            if self._sort_index.lower() == 'asc':
                df = df.sort_index()
            elif self._sort_index.lower() == 'desc':
                df = df.sort_index(ascending=False)
        # fillna
        if self._fillna:
            df = df.fillna(method=self._fillna)
        # 是否丢弃指数相关列
        if self._drop_zs_columns:
            df = df.drop(columns=zs_columns)
        return df

    def _create_readers(self):
        if isinstance(self.symbols, (compat.string_types, int)):
            return [self._reader_type(symbols=self.symbols,
                                      type=self._type,
                                      start=self.start,
                                      end=self.end,
                                      retry_count=self.retry_count,
                                      pause=self.pause,
                                      session=self.session,
                                      chunksize=self.chunksize)]
        else:
            return [self._reader_type(symbols=str(symbol),
                                      type=self._type,
                                      start=self.start,
                                      end=self.end,
                                      retry_count=self.retry_count,
                                      pause=self.pause,
                                      session=self.session,
                                      chunksize=self.chunksize)
                    for symbol in self.symbols]
