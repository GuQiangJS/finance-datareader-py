# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime

import pandas as pd
import pandas.compat as compat
from pandas import read_csv
from pandas.compat import StringIO, bytes_to_str
from pandas_datareader.base import _DailyBaseReader


class SinaDailyDetailsReader(_DailyBaseReader):
    """从 Sina 读取每日成交明细

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
                 end=datetime.date.today() + datetime.timedelta(days=-1), retry_count=3, pause=1, session=None,
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

        不建议传入日期间隔较大的。传入日期较大时会循环按照日期读取，会造成时间较长。

        """
        super(SinaDailyDetailsReader, self).__init__(symbols, start, end, retry_count, pause, session, chunksize)
        self._date = start

    @property
    def url(self):
        # http://market.finance.sina.com.cn/downxls.php?date={0}&symbol={1}{2}
        return 'http://market.finance.sina.com.cn/downxls.php'

    def _get_params(self, *args, **kwargs):
        return {
            'date': self._date.strftime('%Y-%m-%d'),
            'symbol': self._parse_symbol()
        }

    def _parse_symbol(self):
        # 深市前加1，沪市前加0
        return ('sh' if self.symbols[0] == '6' else 'sz') + self.symbols

    def read(self):
        """读取数据

        Returns:
            `pandas.DataFrame`` 实例。`成交时间` 为索引列。

            读取后的数据 **排序顺序为正序**。

        For example:
            ====================  ==========  ==========  =========   ===========   =====
                                     成交价     价格变动    成交量(手)    成交额(元)     性质
            ====================  ==========  ==========  =========   ===========   =====
            2018-06-25 09:25:03     28.25       28.25       5582       15769150      买盘
            2018-06-25 09:30:00     28.24       -0.01       302         852848       卖盘
            2018-06-25 09:30:03     28.26        0.02       6254       17675047      买盘
            2018-06-25 09:30:06     28.28        0.02       1140       3223920       买盘
            ====================  ==========  ==========  =========   ===========   =====

        """
        df = pd.DataFrame()
        self._date = self.start
        while self._date <= self.end:
            df1 = super(SinaDailyDetailsReader, self).read()
            if df1 is not None and not df1.empty:
                df = df.append(df1)
            self._date = self._date + datetime.timedelta(days=1)
        return df

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
                          date_parser=lambda x: pd.to_datetime(x).replace(year=self._date.year,
                                                                          month=self._date.month,
                                                                          day=self._date.day))
            if df is not None and not df.empty:
                df = df.fillna(0).round(2)[::-1]
                return df
        return None
