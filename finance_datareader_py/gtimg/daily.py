# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json

import pandas as pd

from finance_datareader_py import _AbsDailyReader

__all__ = ['GtimgDailyReader']


class GtimgDailyReader(_AbsDailyReader):
    """从 gtimg 读取每日成交汇总数据（支持获取前复权、后复权的数据）

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

    def __init__(self, symbols=None, prefix='', suffix='', type=None,
                 start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        """

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001
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
        super(GtimgDailyReader, self).__init__(symbols, start, end,
                                               retry_count, pause, session,
                                               chunksize)
        self._type = type
        self._prefix = prefix
        self._suffix = suffix

    @property
    def url(self):
        # http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000002,day,2010-01-01,2018-12-31,6400,
        # http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000002,day,2010-01-01,2018-12-31,6400,qfq
        # http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000002,day,2010-01-01,2018-12-31,6400,hfq
        return 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get'

    def _parse_symbol(self):
        # 深市前加sz，沪市前加sh
        if self._prefix:
            return self._prefix + str(self.symbols) + self._suffix
        return ('sh' if str(self.symbols)[0] == '6'
                else 'sz' if str(self.symbols)[0] == '0' or str(self.symbols)[
            0] == '3' else '') + str(self.symbols) + self._suffix

    def _parse_count(self):
        return (self.end - self.start).days + 1

    def _get_params(self, *args, **kwargs):
        f = '%Y-%m-%d'
        return {'param': '{symbol},day,{start},{end},{count},{fq}'.format(
            symbol=self._parse_symbol(), start=self.start.strftime(f),
            end=self.end.strftime(f), fq=self._type if self._type else '',
            count=self._parse_count())}

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
                * Volume: 交易量(手)

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.gtimg.daily import GtimgDailyReader
                >>> df = GtimgDailyReader(symbols='000002').read()
                >>> print(df.tail())

                             Open  Close   High    Low     Volume
                Date
                2018-08-06  21.18  20.86  21.32  20.52   315702.0
                2018-08-07  21.15  21.86  21.86  20.93   451653.0
                2018-08-08  21.89  21.50  22.29  21.50   410720.0
                2018-08-09  21.50  22.48  22.55  21.40   896200.0
                2018-08-10  23.00  23.18  24.07  22.93  1201163.0

        """
        try:
            return super(GtimgDailyReader, self).read()
        finally:
            self.close()

    def _read_url_as_StringIO(self, url, params=None):
        """读取原始数据"""
        response = self._get_response(url, params=params)
        txt = GtimgDailyReader._get_split_txt(response.text)
        if not txt:
            return pd.DataFrame()
        pd_data = pd.DataFrame(json.loads(txt))
        return pd_data

    def _get_split_txt(txt):
        """自动截取文本中的每日数据。（区分前复权、后复权、不复权）"""
        s_txts = ['"qfqday":', '"hfqday":', '"day":']
        e_txt = ']]'
        for s_txt in s_txts:
            if txt.__contains__(s_txt) and txt.__contains__(e_txt):
                return txt[txt.index(s_txt) + len(s_txt):
                           txt.rindex(e_txt) + len(e_txt)]
        return ''

    def _read_lines(self, out):
        """加工原始数据"""
        if out.empty:
            return out
        # 设置标题
        out.rename(
            columns={0: 'Date', 1: 'Open', 2: 'Close', 3: 'High', 4: 'Low',
                     5: 'Volume'}, inplace=True)
        if 6 in out:
            out.drop([6], axis=1, inplace=True)
        # 转换 Date 列为 datetime 数据类型
        out['Date'] = pd.to_datetime(out['Date'])
        # out['涨跌幅'] = out['涨跌幅'].str.replace('%', '')
        # out['换手率'] = out['换手率'].str.replace('%', '')
        # 将 Date 列设为索引列
        out.set_index("Date", inplace=True)
        out = self._convert_numeric_allcolumns(out)
        return out
