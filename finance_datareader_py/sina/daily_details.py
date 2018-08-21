# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime

import pandas as pd
from pandas import read_csv

from finance_datareader_py import _AbsDailyReader
from finance_datareader_py.sina import _parse_symbol


class SinaDailyDetailsReader(_AbsDailyReader):
    """从 Sina 读取每日成交明细

    .. warning::

        Sina 已下线该功能。

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        start: 开始日期。默认值：2004-10-08
        end: 结束日期。默认值：当前日期的 **前一天** 。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:
    """

    def __init__(self, symbols: str = None, start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        """

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
            start: 开始日期。默认值：2004-10-08
            end: 结束日期。默认值：当前日期的 **前一天** 。
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:

        .. warning::
            不建议传入日期间隔较大的。传入日期较大时会循环按照日期读取，会造成时间较长。

        """
        super(SinaDailyDetailsReader, self).__init__(symbols, start, end,
                                                     retry_count, pause,
                                                     session, chunksize)
        self._date = start
        # 解析 url 回传内容时，如果长度小于等于200，被认为是无效数据
        self._read_url_as_StringIO_min_len = 200
        # 解析 url 回传内容时使用的字符编码
        self._encoding = 'gb2312'

    @property
    def url(self):
        # http://market.finance.sina.com.cn/downxls.php?date={0}&symbol={1}{2}
        return 'http://market.finance.sina.com.cn/downxls.php'

    def _get_params(self, *args, **kwargs):
        return {
            'date': self._date.strftime('%Y-%m-%d'),
            'symbol': _parse_symbol(self.symbols)
        }

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame``:

            无数据时返回空白的 ``pandas.DataFrame`` 。参见 ``pandas.DataFrame.empty``。

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.sina.daily_details import SinaDailyDetailsReader

                >>> import datetime

                >>> df = SinaDailyDetailsReader(symbols='000002', start=datetime.date(2018, 7, 2), end=datetime.date(2018, 7, 2)).read()

                >>> print(df.tail())

                Empty DataFrame
                Columns: []
                Index: []

        """
        try:
            df = pd.DataFrame()
            self._date = self.start
            while self._date <= self.end:
                df1 = super(SinaDailyDetailsReader, self).read()
                if df1 is not None and not df1.empty:
                    df = df.append(df1)
                self._date = self._date + datetime.timedelta(days=1)
            return df
        finally:
            self.close()

    def _read_lines(self, out):
        if out:
            df = read_csv(out, sep=r'\t', index_col=0, parse_dates=[0],
                          na_values=('--', 'null'), engine='python',
                          date_parser=lambda x: pd.to_datetime(x).replace(
                              year=self._date.year,
                              month=self._date.month,
                              day=self._date.day))
            if df is not None and not df.empty:
                df = df.fillna(0).round(2)[::-1]
                df = self._convert_numeric_allcolumns(df)
                return df
        return None
