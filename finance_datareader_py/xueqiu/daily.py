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
            ``pandas.DataFrame`` 实例。``Date`` 列为索引列。

            成交金额的单位为 *元*。

            读取后的数据 **排序顺序为正序**。最新日期排在最后面。

        示例::
            日期    成交金额   Open   High    Low  Close   涨跌额   涨跌幅   换手率

            2018-06-26  67234728  25.50  25.51  23.81  24.22 -1.32 -5.17  0.69
            2018-06-27  46251282  23.86  24.57  23.50  23.88 -0.34 -1.40  0.47
            2018-06-28  35288491  24.10  24.60  23.89  24.60  0.72  3.02  0.36
            2018-07-01  84620386  24.50  24.55  22.52  22.80 -1.80 -7.32  0.87
            2018-07-02  54996488  23.10  23.48  22.80  23.42  0.62  2.72  0.56
            2018-07-03  24988103  23.46  23.75  23.00  23.00 -0.42 -1.79  0.25
            2018-07-04  26727861  23.02  23.41  22.85  23.05  0.05  0.22  0.27
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
