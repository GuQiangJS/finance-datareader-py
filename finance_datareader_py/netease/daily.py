# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>


import datetime

import pandas.compat as compat
from pandas.compat import StringIO, bytes_to_str
from pandas_datareader.base import _DailyBaseReader, _BaseReader


class NetEaseDailyReader(_DailyBaseReader):
    """从 163 读取每日成交汇总数据

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        start: 开始日期。默认值：2004-10-08
        end: 结束日期。默认值：当前日期的 **前一天** 。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:
    """

    def __init__(self, symbols=None, start=datetime.date(2004, 10, 8),
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

        Todo:
            暂时未能实现抓取指数的功能，抓取指数可以使用 ``finance-datareader-py.sohu.daily.SohuDailyReader``
        """
        super(NetEaseDailyReader, self).__init__(symbols, start, end, retry_count, pause, session, chunksize)

    @property
    def url(self):
        # http://quotes.money.163.com/trade/lsjysj_002024.html#06f01
        # http://quotes.money.163.com/service/chddata.html?code=1002024&start=20040707&end=20180629&fields=TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER
        # http://quotes.money.163.com/service/chddata.html?code=0601398&start=20061027&end=20180628&fields=TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER
        return 'http://quotes.money.163.com/service/chddata.html?code={symbol}&start={start}&end={end}&fields=TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER'.format(
            symbol=self._parse_symbol(), start=self.start.strftime('%Y%m%d'), end=self.end.strftime('%Y%m%d'))

    def _parse_symbol(self):
        # 深市前加1，沪市前加0
        return ('0' if self.symbols[0] == '6' else '1') + self.symbols

    def _get_params(self, *args, **kwargs):
        return ''

    def _read_url_as_StringIO(self, url, params=None):
        response = self._get_response(url, params=params)
        text = self._sanitize_response(response)
        out = StringIO()
        if len(text) == 0:
            service = self.__class__.__name__
            raise IOError("{} request returned no data; check URL for invalid "
                          "inputs: {}".format(service, self.url))
        if isinstance(text, compat.binary_type):
            out.write(bytes_to_str(text, encoding='GB2312'))
        else:
            out.write(text)
        out.seek(0)
        return out

    def _read_lines(self, out):
        out = _BaseReader._read_lines(self, out)
        out = out.drop(['股票代码', '名称'], axis=1)
        out.rename(
            columns={'日期': 'Date', '开盘价': 'Open', '收盘价': 'Close', '涨跌额': 'Change', '涨跌幅': 'Quote', '最低价': 'Low',
                     '最高价': 'High', '成交量': 'Volume',
                     '成交金额': 'Turnover', '换手率': 'Rate'}, inplace=True)
        out['Volume'] = (out['Volume'] / 100).round(0)
        out['Turnover'] = (out['Turnover'] / 10000).round(0)
        return out

    def read(self):
        """读取数据

        Returns:
            `pandas.DataFrame`_ 实例。``Date`` 列为索引列。

            成交量的单位为 *手*，成交金额的单位为 *万元*。

            读取后的数据 **排序顺序为倒序**。最新日期排在最前面。

            =========  =====
            列名        解释
            =========  =====
            Date       日期
            Open       开盘价
            Close      收盘价
            Change     涨跌额
            Quote      涨跌幅
            High       最高价
            Low        最低价
            Turnover   成交金额
            Rate       换手率
            =========  =====

        For example:
            ==========  ======  ====== ======  =====  =======  ========  =========  =========  ==========
                  Date   Close   High    Low   Open    Change    Quote    Rate       Volume      Turnover
            ==========  ======  ====== ======  =====  =======  ========  =========  =========  ==========
            2004-10-08   5.56   5.60   5.28     5.42    0.14      2.583    0.7425   117074.0       6369.0
            2004-10-11   5.54   5.65   5.51     5.56   -0.02    -0.3597    1.6744   264020.0      34637.0
            2004-10-12   5.79   5.87   5.50     5.53    0.25     4.5126    3.8106   600869.0      14604.0
            ==========  ======  ====== ======  =====  =======  ========  =========  =========  ==========

        .. pandas.DataFrame:
            https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html

        """
        return super(NetEaseDailyReader, self).read()
