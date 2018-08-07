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

    def __init__(self, symbols=None, type=None,
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
        super(GtimgDailyReader, self).__init__(symbols, start, end,
                                               retry_count, pause, session,
                                               chunksize)
        self._type = type

    @property
    def url(self):
        # http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000002,day,2010-01-01,2018-12-31,6400,
        # http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000002,day,2010-01-01,2018-12-31,6400,qfq
        # http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000002,day,2010-01-01,2018-12-31,6400,hfq
        return 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get'

    def _parse_symbol(self):
        # 深市前加sz，沪市前加sh
        return ('sh' if self.symbols[0] == '6' else 'sz') + self.symbols

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

        Examples:
            .. code-block:: python

                from finance_datareader_py.gtimg.daily import GtimgDailyReader

                df = GtimgDailyReader(symbols='000002').read()
                # 后复权
                # df = GtimgDailyReader(symbols='000002', type='hfq').read()
                # 前复权
                # df = GtimgDailyReader(symbols='000002', type='qfq').read()

                print(df)

            .. code-block::

                日期          Open   Close    High     Low      交易量(手)
                2004-10-08   5.420   5.560   5.600   5.280  117073.850
                2004-10-11   5.560   5.540   5.650   5.510  264020.250
                2004-10-12   5.530   5.790   5.870   5.500  600868.640
                ...            ...     ...     ...     ...         ...
                2018-07-03  23.100  23.420  23.480  22.800  549964.000
                2018-07-04  23.460  23.000  23.750  23.000  249881.000
                2018-07-05  23.020  23.050  23.410  22.850  267278.000

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
            columns={0: '日期', 1: 'Open', 2: 'Close', 3: 'High', 4: 'Low',
                     5: '交易量(手)'}, inplace=True)
        if 6 in out:
            out.drop([6], axis=1, inplace=True)
        # 转换 Date 列为 datetime 数据类型
        out['日期'] = pd.to_datetime(out['日期'])
        # out['涨跌幅'] = out['涨跌幅'].str.replace('%', '')
        # out['换手率'] = out['换手率'].str.replace('%', '')
        # 将 Date 列设为索引列
        out.set_index("日期", inplace=True)
        out = self._convert_numeric_allcolumns(out)
        return out
