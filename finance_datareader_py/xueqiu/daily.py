# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json

import pandas as pd
import requests
from pandas_datareader.base import _DailyBaseReader

__all__ = ['XueQiuDailyReader']


class XueQiuDailyReader(_DailyBaseReader):
    """从 雪球 读取每日成交汇总数据（可直接获取前复权、后复权的数据）

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002
        type:
            * default: 不复权（默认）
            * before: 前复权
            * after: 后复权
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
            type:
                * default: 不复权（默认）
                * before: 前复权
                * after: 后复权
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
            ``pandas.DataFrame`` 实例。``成交时间`` 列为索引列。

            读取后的数据 **排序顺序为倒序**。

        Examples:
            .. testcode:: python

                from finance_datareader_py.xueqiu.daily import XueQiuDailyReader

                df = XueQiuDailyReader(symbols='000002', start=datetime.date(2010, 1, 1)).read()

                print(df)

            .. testoutput::

                成交时间        成交价格  价格变动  成交量(手)    成交额(元)   性质
                2018-07-02 15:00:04  22.80  0.01    5763  13139640   卖盘
                2018-07-02 14:57:00  22.79  0.00       9     20511   卖盘
                2018-07-02 14:56:57  22.79  0.00      98    225241   买盘
                2018-07-02 14:56:54  22.79  0.00     171    389700   买盘

        """
        try:
            return super(XueQiuDailyReader, self).read()
        finally:
            self.close()

    def _read_url_as_StringIO(self, url, params=None):
        """
        从 sohu 读取原始数据
        :param url:
        :param params:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '66.0.3359.181 Safari/537.36'}
        if self.session:
            self.session.cookies = requests.get('http://www.xueqiu.com',
                                                headers=headers).cookies
        response = self._get_response(url, params=params, headers=headers)
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
        """
        加工原始数据
        :param out:
        :return:
        """
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
        return out
