# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json

import pandas as pd

from finance_datareader_py import _AbsDailyReader

__all__ = ['XueQiuDailyReader']


class XueQiuDailyReader(_AbsDailyReader):
    """从 雪球 读取每日成交汇总数据（支持获取前复权、后复权的数据）

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002
        type: {'default', 'before', 'after'}, 默认值 'default'

            * 'default': 不复权（默认）
            * 'before': 前复权
            * 'after': 后复权

        start: 开始日期。默认值：2004-10-08
        end: 结束日期。默认值：当前日期的 **前一天** 。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:
    """

    def __init__(self, symbols=None, type='default',
                 start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        """

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001
            type: {'default', 'before', 'after'}, 默认值 'default'

                * 'default': 不复权（默认）
                * 'before': 前复权
                * 'after': 后复权

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
        self._type = type

    @property
    def url(self):
        # https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ000002
        # &begin=1092067200000&period=day&type=after&count=107800
        return 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' \
               '{symbol}&begin={begin}&period=day&type={type}&count={count}' \
            .format(symbol=self._parse_symbol(), begin=self._paser_start(),
                    type=self._type, count=self._parse_count())

    def _parse_symbol(self):
        # 深市前加sz，沪市前加sh
        return ('SH' if self.symbols[0] == '6' else 'SZ') + self.symbols

    def _paser_start(self):
        """转换 self.start 为时间戳格式。使用13位时间戳格式

        :return:
        """
        return round(self.start.timestamp() * 1000)

    def _parse_count(self):
        return (self.end - self.start).days + 1

    def _get_params(self, *args, **kwargs):
        return {}

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame``:

            无数据时返回空白的 ``pandas.DataFrame`` 。参见 ``pandas.DataFrame.empty``。

        Examples:
            .. testcode:: python

                from finance_datareader_py.xueqiu.daily import XueQiuDailyReader

                df = XueQiuDailyReader(symbols='000002', start=datetime.date(2010, 1, 1)).read()

                print(df)

            .. testoutput::

                日期             成交金额   Open   High    Low  Close   涨跌额   涨跌幅   换手率
                2010-01-03   96983253  10.85  10.87  10.60  10.60 -0.21 -1.94  1.00
                2010-01-04  184862078  10.51  10.52  10.20  10.36 -0.24 -2.26  1.91
                2010-01-05  135860406  10.35  10.51  10.20  10.36  0.00  0.00  1.41
                2010-01-06  115244198  10.36  10.43  10.24  10.28 -0.08 -0.77  1.19
                2010-01-07  108530422  10.28  10.38  10.19  10.35  0.07  0.68  1.12

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
            columns={0: '日期', 1: '成交金额', 2: 'Open', 3: 'High', 4: 'Low',
                     5: 'Close',
                     # 2: (('Adj ' if self._type != 'default' else '') + 'Open'),
                     # 3: (('Adj ' if self._type != 'default' else '') + 'High'),
                     # 4: (('Adj ' if self._type != 'default' else '') + 'Low'),
                     # 5: (('Adj ' if self._type != 'default' else '') + 'Close'),
                     6: '涨跌额', 7: '涨跌幅', 8: '换手率'}, inplace=True)
        # 转换 Date 列为 datetime 数据类型
        out['日期'] = pd.to_datetime(out['日期'], unit='ms').dt.date
        # out['涨跌幅'] = out['涨跌幅'].str.replace('%', '')
        # out['换手率'] = out['换手率'].str.replace('%', '')
        # 将 Date 列设为索引列
        out.set_index("日期", inplace=True)
        out = self._convert_numeric_allcolumns(out)
        return out
