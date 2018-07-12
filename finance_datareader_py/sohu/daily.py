# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json

import pandas as pd
from pandas.io.json import json_normalize

from finance_datareader_py import _AbsDailyReader

__all__ = ['SohuDailyReader']


class SohuDailyReader(_AbsDailyReader):
    """从sohu读取每日成交汇总数据

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        prefix: 读取股票数据时需要拼接的前缀。默认为 ``cn_``。如果是获取指数时需要使用 ``zs_``。
        start: 开始日期。默认值：2004-10-08
        end: 结束日期。默认值：当前日期的 **前一天** 。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:
    """

    def __init__(self, symbols=None, prefix='cn_',
                 start=datetime.date(2004, 10, 8),
                 end=datetime.date.today() + datetime.timedelta(days=-1),
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        """

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
            prefix: 读取股票数据时需要拼接的前缀。默认为 'cn_'。如果是获取指数时需要使用 'zs_'。
            start: 开始日期。默认值：2004-10-08
            end: 结束日期。默认值：当前日期的 **前一天** 。
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:
        """
        super(SohuDailyReader, self).__init__(symbols, start, end, retry_count,
                                              pause, session, chunksize)
        self.prefix = prefix

    @property
    def url(self):
        # http://q.stock.sohu.com/hisHq?code=cn_600569&start=20041008&end=20180608&stat=1&order=D&period=d&rt=jsonp
        return 'http://q.stock.sohu.com/hisHq?code={symbol}&start={start}&end={end}&stat=1&order=D&period=d&rt=jsonp'.format(
            symbol=self._parse_symbol(), start=self.start.strftime('%Y%m%d'),
            end=self.end.strftime('%Y%m%d'))

    def _parse_symbol(self):
        return self.prefix + self.symbols

    def _get_params(self, *args, **kwargs):
        return ''

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame`` 实例。

            成交量的单位为 *手*，成交金额的单位为 *万元*。

            无数据时返回空白的 ``pandas.DataFrame`` 。参见 ``pandas.DataFrame.empty``。

        Examples:
            .. testcode:: python

                from finance_datareader_py.sohu.daily import SohuDailyReader

                # df = SohuDailyReader(symbols='399300', prefix='zs_').read() # 获取指数数据
                df2 = SohuDailyReader(symbols='000002').read()

                print(df2)

            .. testoutput::

                Date        Open  Close Change  Quote    Low   High  Volume   Turnover  Rate
                2018-07-05  23.02  23.05   0.05   0.22  22.85  23.41  267279   61939.30  0.28
                2018-07-04  23.46  23.00  -0.42  -1.79  23.00  23.75  249881   58247.02  0.26
                2018-07-03  23.10  23.42   0.62   2.72  22.80  23.48  549965  127402.35  0.57
        """
        try:
            return super(SohuDailyReader, self).read()
        finally:
            self.close()

    def _read_url_as_StringIO(self, url, params=None):
        """
        从 sohu 读取原始数据
        :param url:
        :param params:
        :return:
        """
        response = self._get_response(url, params=params)
        txt = str(self._sanitize_response(response), encoding='ISO-8859-9')
        data_json = json.loads(txt[9:-2])
        pd_data = json_normalize(data_json[0], record_path='hq')
        return pd_data

    def _read_lines(self, out):
        """
        加工原始数据
        :param out:
        :return:
        """
        # 设置标题
        out.rename(
            columns={0: 'Date', 1: 'Open', 2: 'Close', 3: 'Change', 4: 'Quote',
                     5: 'Low', 6: 'High', 7: 'Volume',
                     8: 'Turnover', 9: 'Rate'}, inplace=True)
        # 转换 Date 列为 datetime 数据类型
        out['Date'] = pd.to_datetime(out['Date'], format='%Y-%m-%d')
        out['Quote'] = out['Quote'].str.replace('%', '')
        out['Rate'] = out['Rate'].str.replace('%', '')
        # 将 Date 列设为索引列
        out.set_index("Date", inplace=True)
        out = self._convert_numeric_allcolumns(out)
        return out
