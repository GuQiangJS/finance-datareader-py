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
            .. code-block:: python

                >>> from finance_datareader_py.sohu.daily import SohuDailyReader

                >>> df = SohuDailyReader(symbols='000002').read()

                >>> print(df.tail())

                            Open  Close  Change  Quote   Low  High    Volume  Turnover  Rate
                Date
                2004-10-14  5.80   5.67   -0.12  -2.07  5.56  5.80  265167.0  15041.02  1.68
                2004-10-13  5.81   5.79    0.00   0.00  5.69  5.85  252039.0  14604.28  1.60
                2004-10-12  5.53   5.79    0.25   4.51  5.50  5.87  600869.0  34637.16  3.82
                2004-10-11  5.56   5.54   -0.02  -0.36  5.51  5.65  264020.0  14775.34  1.68
                2004-10-08  5.42   5.56    0.14   2.58  5.28  5.60  117074.0   6368.60  0.74
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
