# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json

import pandas as pd

from finance_datareader_py import _AbsDailyReader
from finance_datareader_py import xueqiu

__all__ = ['XueQiuDailyReader']


class XueQiuDailyReader(_AbsDailyReader):
    """从 雪球 读取每日成交汇总数据（支持获取前复权、后复权的数据）

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002
        prefix: 股票代码前缀。默认为空。

            * 为空表示会自动根据股票代码判断。
            * 对于某些特定指数请填写 `sz` 或 `sh`。

        suffix: 股票代码后缀。默认为空。

            * 为空表示会自动根据股票代码判断。
            * 对于某些特定指数请自行填写。

        type: {None, 'qfq', 'hfq'}, 默认值 None

            * None: 不复权（默认）
            * 'qfq': 前复权
            * 'hfq': 后复权

        start: 开始日期。默认值：2004-10-08
        end: 结束日期。默认值：当前日期的 **前一天** 。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:
    """

    def __init__(self, symbols=None, prefix='', suffix='', type='default',
                 start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        """

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001
            type: {None, 'qfq', 'hfq'}, 默认值 None

                * None: 不复权（默认）
                * 'qfq': 前复权
                * 'hfq': 后复权

            start: 开始日期。默认值：2004-10-08
            end: 结束日期。默认值：当前日期的 **前一天** 。
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:
        """
        super(XueQiuDailyReader, self).__init__(symbols, start, end,
                                                retry_count,
                                                pause, session, chunksize)
        self._type = 'default'
        if not type:
            if str(type).lower() == 'qfq':
                self._type = 'before'
            elif str(type).lower() == 'hfq':
                self._type = 'after'
        self._prefix = prefix
        self._suffix = suffix

    @property
    def url(self):
        # https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ000002
        # &begin=1092067200000&period=day&type=after&count=107800
        return 'https://stock.xueqiu.com/v5/stock/chart/kline.json'

    def _paser_start(self):
        """转换 self.start 为时间戳格式。使用13位时间戳格式

        :return:
        """
        return round(self.start.timestamp() * 1000)

    def _parse_count(self):
        return (self.end - self.start).days + 1

    def _get_params(self, *args, **kwargs):
        return {'symbol': xueqiu._parse_symbol(self.symbols, self._prefix,
                                               self._suffix),
                'begin': self._paser_start(),
                'type': self._type, 'count': self._parse_count()}

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame``:

            无数据时返回空白的 ``pandas.DataFrame`` 。参见 ``pandas.DataFrame.empty``。

            部分返回列名说明：

                * Open:开盘价
                * Close: 收盘价
                * High: 最高价
                * Low: 最低价
                * Turnover: 成交金额
                * Rate: 换手率

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.xueqiu.daily import XueQiuDailyReader
                >>> import datetime
                >>> df = XueQiuDailyReader(symbols='000002', start=datetime.date(2010, 1, 1)).read()
                >>> print(df.tail())

                            Turnover   Open   High    Low  Close   涨跌额   涨跌幅   Rate
                Date
                2018-08-06   45165309.0  21.15  21.86  20.93  21.86  1.00  4.79  0.46
                2018-08-07   41072018.0  21.89  22.29  21.50  21.50 -0.36 -1.65  0.42
                2018-08-08   89620017.0  21.50  22.55  21.40  22.48  0.98  4.56  0.91
                2018-08-09  120116303.0  23.00  24.07  22.93  23.18  0.70  3.11  1.23
                2018-08-12   48949476.0  22.60  23.21  22.46  23.04 -0.14 -0.60  0.50

        """
        try:
            return super(XueQiuDailyReader, self).read()
        finally:
            self.close()

    def _read_url_as_StringIO(self, url, params=None):
        if self.session:
            self.session.cookies = self._get_cookie('http://www.xueqiu.com')
        response = self._get_response(url, params=params)
        # txt = str(self._sanitize_response(response))
        s_txt, e_txt = '"item":', ']]'
        txt = response.text
        if txt.__contains__(s_txt) and txt.__contains__(e_txt):
            txt = txt[txt.index(s_txt) + len(s_txt):txt.rindex(e_txt) + len(
                e_txt)]
        else:
            return pd.DataFrame()
        # data_json = json.loads(txt[9:-2])
        pd_data = pd.DataFrame(json.loads(txt))
        return pd_data

    def _read_lines(self, out):
        """加工原始数据"""
        if out.empty:
            return out
        # 设置标题
        out.rename(
            columns={0: 'Date', 1: 'Turnover', 2: 'Open', 3: 'High', 4: 'Low',
                     5: 'Close',
                     6: '涨跌额', 7: '涨跌幅', 8: 'Rate'}, inplace=True)
        # 转换 Date 列为 datetime 数据类型
        out['Date'] = pd.to_datetime(out['Date'], unit='ms').dt.date
        # out['涨跌幅'] = out['涨跌幅'].str.replace('%', '')
        # out['换手率'] = out['换手率'].str.replace('%', '')
        # 将 Date 列设为索引列
        out.set_index("Date", inplace=True)
        out = self._convert_numeric_allcolumns(out)
        return out
