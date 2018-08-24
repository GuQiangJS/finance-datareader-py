# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>


import datetime

from pandas_datareader.base import _BaseReader

from finance_datareader_py import _AbsDailyReader

__all__ = ['NetEaseDailyReader']


class NetEaseDailyReader(_AbsDailyReader):
    """从 网易 读取每日成交汇总数据

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        prefix: 股票代码前缀。默认为空。

            * 为空表示会自动根据股票代码判断。
            * 对于某些特定指数请填写 `sz` 或 `sh`。

        suffix: 股票代码后缀。默认为空。

            * 为空表示会自动根据股票代码判断。
            * 对于某些特定指数请自行填写。

        start: 开始日期。默认值：2004-10-08
        end: 结束日期。默认值：当前日期的 **前一天** 。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:
    """

    def __init__(self, symbols: str = None, prefix='', suffix='',
                 start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        """

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
            prefix: 股票代码前缀。默认为空。

                * 为空表示会自动根据股票代码判断。
                * 对于某些特定指数请填写 `sz` 或 `sh`。

            suffix: 股票代码后缀。默认为空。

                * 为空表示会自动根据股票代码判断。
                * 对于某些特定指数请自行填写。

            start: 开始日期。默认值：2004-10-08
            end: 结束日期。默认值：当前日期的 **前一天** 。
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:

        """
        super(NetEaseDailyReader, self).__init__(symbols, start, end,
                                                 retry_count, pause, session,
                                                 chunksize)
        # 解析 url 回传内容时使用的字符编码
        self._encoding = 'gb2312'
        self._prefix = prefix
        self._suffix = suffix

    @property
    def url(self):
        # http://quotes.money.163.com/service/chddata.html?code=1002024
        # &start=20040707&end=20180629
        # &fields=TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER
        # http://quotes.money.163.com/service/chddata.html?code=0601398
        # &start=20061027&end=20180628
        # &fields=TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER
        return 'http://quotes.money.163.com/service/chddata.html'

    def _parse_symbol(self):
        r = ''
        if self._prefix:
            r = self._prefix + self.symbols
        # 深市前加1，沪市前加0
        r = ('0' if self.symbols[0] == '6' else '1') + self.symbols
        return r + self._suffix

    def _get_params(self, *args, **kwargs):
        return {'code': self._parse_symbol(),
                'start': self.start.strftime('%Y%m%d'),
                'end': self.end.strftime('%Y%m%d'),
                'fields': 'TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;TURNOVER;VOTURNOVER'
                          ';VATURNOVER'}

    def _read_lines(self, out):
        out = _BaseReader._read_lines(self, out)
        out = out.drop(['股票代码', '名称'], axis=1)
        out.rename(
            columns={'日期': 'Date', '开盘价': 'Open', '收盘价': 'Close',
                     '涨跌额': 'Change', '涨跌幅': 'Quote',
                     '最低价': 'Low', '最高价': 'High', '成交量': 'Volume',
                     '成交金额': 'Turnover', '换手率': 'Rate'
                     }, inplace=True)
        out['Volume'] = (out['Volume'] / 100).round(0)
        out['Turnover'] = (out['Turnover'] / 10000).round(0)
        return out

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame``:

            成交量的单位为 *手*，成交金额的单位为 *万元*。

            无数据时返回空白的 ``pandas.DataFrame`` 。参见 ``pandas.DataFrame.empty``。

            部分返回列名说明：

                * Open:开盘价
                * Close: 收盘价
                * High: 最高价
                * Low: 最低价
                * Volume: 交易量(手)
                * Turnover: 成交金额
                * Rate: 换手率

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.netease.daily import NetEaseDailyReader
                >>> print(NetEaseDailyReader(symbols='000002').read().tail())

                            Close   High    Low   Open Change    Quote    Rate     Volume  Turnover

                2018-08-06  20.86  21.32  20.52  21.18  -0.22  -1.0436  0.3247   315702.0   66288.0
                2018-08-07  21.86  21.86  20.93  21.15    1.0   4.7939  0.4645   451653.0   96917.0
                2018-08-08  21.50  22.29  21.50  21.89  -0.36  -1.6468  0.4224   410720.0   90302.0
                2018-08-09  22.48  22.55  21.40  21.50   0.98   4.5581  0.9216   896200.0  199710.0
                2018-08-10  23.18  24.07  22.93  23.00    0.7   3.1139  1.2352  1201163.0  282009.0

        """
        try:
            return super(NetEaseDailyReader, self).read()
        finally:
            self.close()
