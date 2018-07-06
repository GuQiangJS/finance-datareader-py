# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime

import pandas as pd
import pandas.compat as compat
from pandas import read_csv
from pandas.compat import StringIO, bytes_to_str
from pandas_datareader.base import _DailyBaseReader


class GtimgDailyDetailsReader(_DailyBaseReader):
    """从 gtimg 读取每日成交明细

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

        Warnings:
            不建议传入日期间隔较大的。传入日期较大时会循环按照日期读取，会造成时间较长。

        """
        super(GtimgDailyDetailsReader, self).__init__(symbols, start, end,
                                                      retry_count, pause,
                                                      session, chunksize)
        self._date = start

    @property
    def url(self):
        # http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sz000002&d=20180704
        return 'http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c={0}&d={1}'.format(
            self._parse_symbol(), self._date.strftime('%Y%m%d'))

    def _get_params(self, *args, **kwargs):
        return {}

    def _parse_symbol(self):
        # 深市前加1，沪市前加0
        return ('sh' if self.symbols[0] == '6' else 'sz') + self.symbols

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame`` 实例。``成交时间`` 为索引列。

            读取后的数据 **排序顺序为倒序**。

            *无数据时返回空白的 `DataFrame` 。参见 `DataFrame.empty`。*

        Examples:
            .. testcode:: python

                from finance_datareader_py.gtimg.daily_details import GtimgDailyDetailsReader

                df = GtimgDailyDetailsReader(symbols='000002', start=datetime.date(2018, 7, 2),
                                             end=datetime.date(2018, 7, 2)).read()

                print(df)

            .. testoutput::

                成交时间        成交价格  价格变动  成交量(手)    成交额(元)   性质
                2018-07-02 15:00:04  22.80  0.01    5763  13139640   卖盘
                2018-07-02 14:57:00  22.79  0.00       9     20511   卖盘
                2018-07-02 14:56:57  22.79  0.00      98    225241   买盘
                2018-07-02 14:56:54  22.79  0.00     171    389700   买盘

        """
        try:
            df = pd.DataFrame()
            self._date = self.start
            while self._date <= self.end:
                df1 = super(GtimgDailyDetailsReader, self).read()
                if df1 is not None and not df1.empty:
                    df = df.append(df1)
                self._date = self._date + datetime.timedelta(days=1)
            return df
        finally:
            self.close()

    def _read_url_as_StringIO(self, url, params=None):
        """
        Open url (and retry)
        """
        response = self._get_response(url, params=params)
        text = self._sanitize_response(response)
        out = StringIO()
        if len(text) <= 200:
            # 今日没有数据
            return None
        if isinstance(text, compat.binary_type):
            out.write(bytes_to_str(text, encoding='gb2312'))
        else:
            out.write(text)
        out.seek(0)
        return out

    def _read_lines(self, out):
        if out:
            # return read_csv(out,sep=r'\t',index_col=0,parse_dates=[0],na_values=('--', 'null'),date_parser=self._date_parser)
            df = read_csv(out, sep=r'\t', index_col=0, parse_dates=[0],
                          na_values=('--', 'null'), engine='python',
                          date_parser=lambda x: pd.to_datetime(x).replace(
                              year=self._date.year,
                              month=self._date.month,
                              day=self._date.day))
            if df is not None and not df.empty:
                df = df.fillna(0).round(2)[::-1]
                return df
        return None
