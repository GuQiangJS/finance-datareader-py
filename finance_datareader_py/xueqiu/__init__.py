# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime

import pandas as pd

from finance_datareader_py import _AbsDailyReader


def _parse_symbol(symbol):
    # 深市前加sz，沪市前加sh
    return ('SH' if symbol[0] == '6' else 'SZ') + symbol


class FinancialIndicatorReader(_AbsDailyReader):
    """从 雪球 读取主要财务指标

    **从1990-01-01开始获取数据**。

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:

    Returns:
        ``DataFrame``: 结果按照 公告日期**倒序** 排序。 任意数据表无数据时返回 空白的
        ``pandas.DataFrame`` 。 参见 ``pandas.DataFrame.empty``。

        输出列集合：
        .. code-block:: json
            [
                "基本每股收益",
                "期末现金及现金等价物余额",
                "现金及现金等价物净增加额",
                "汇率变动对现金及现金等价物的影响",
                "净资产收益率(摊薄)(%)",
                "每股收益(摊薄)",
                "每股收益(加权)",
                "筹资活动产生的现金流量净额",
                "投资活动产生的现金流量净额",
                "主营业务收入",
                "主营业务收入增长率(%)",
                "主营业务利润",
                "每股净资产",
                "净资产增长率(%)",
                "净利润增长率(%)",
                "净利润",
                "每股现金流",
                "经营活动产生的现金流量净额",
                "每股经营性现金流",
                "销售毛利率(%)",
                "资产总额",
                "负债总额",
                "总资产增长率(%)",
                "利润总额",
                "股东权益合计",
                "净资产收益率(加权)(%)"
            ]

    Examples:
        .. code-block:: python

            >>> from finance_datareader_py.xueqiu import FinancialIndicatorReader
            >>> df = FinancialIndicatorReader('601398').read()
            >>> print(df.iloc[0][0:5])

            基本每股收益                     0.22
            期末现金及现金等价物余额        1.46277e+12
            现金及现金等价物净增加额         -5.756e+10
            汇率变动对现金及现金等价物的影响     -2.518e+10
            净资产收益率(摊薄)(%)               NaN
            Name: 2018-03-31 00:00:00, dtype: object
    """

    def __init__(self, symbols=None, retry_count=3, pause=1, session=None,
                 chunksize=25):
        """从 雪球 读取主要财务指标

        **从1990-01-01开始获取数据**。

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:

        Returns:
            ``DataFrame``: 结果按照 公告日期**倒序** 排序。 任意数据表无数据时返回 空白的
            ``pandas.DataFrame`` 。 参见 ``pandas.DataFrame.empty``。

            输出列集合：
            .. code-block:: json
                [
                    "基本每股收益",
                    "期末现金及现金等价物余额",
                    "现金及现金等价物净增加额",
                    "汇率变动对现金及现金等价物的影响",
                    "净资产收益率(摊薄)(%)",
                    "每股收益(摊薄)",
                    "每股收益(加权)",
                    "筹资活动产生的现金流量净额",
                    "投资活动产生的现金流量净额",
                    "主营业务收入",
                    "主营业务收入增长率(%)",
                    "主营业务利润",
                    "每股净资产",
                    "净资产增长率(%)",
                    "净利润增长率(%)",
                    "净利润",
                    "每股现金流",
                    "经营活动产生的现金流量净额",
                    "每股经营性现金流",
                    "销售毛利率(%)",
                    "资产总额",
                    "负债总额",
                    "总资产增长率(%)",
                    "利润总额",
                    "股东权益合计",
                    "净资产收益率(加权)(%)"
                ]

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.xueqiu import FinancialIndicatorReader
                >>> df = FinancialIndicatorReader('601398').read()
                >>> print(df.iloc[0][0:5])

                基本每股收益                     0.22
                期末现金及现金等价物余额        1.46277e+12
                现金及现金等价物净增加额         -5.756e+10
                汇率变动对现金及现金等价物的影响     -2.518e+10
                净资产收益率(摊薄)(%)               NaN
                Name: 2018-03-31 00:00:00, dtype: object
        """
        super(FinancialIndicatorReader, self).__init__(symbols, None, None,
                                                       retry_count, pause,
                                                       session,
                                                       chunksize)
        self._format = 'json'

    @property
    def url(self):
        # https://xueqiu.com/stock/f10/finmainindex.json?symbol=SH601398&page=1&size=200&_=1535004918077
        return 'https://xueqiu.com/stock/f10/finmainindex.json'

    def _get_params(self, *args, **kwargs):
        # 计算从 1990-01-01 至今一共有多少个月
        n = datetime.date.today()
        s = datetime.date(1990, 1, 1)
        m = (n.year - s.year) * 12 + n.month
        # 每四个月才会有一次数据
        return {'symbol': _parse_symbol(self.symbols), 'size': int(m / 4 + 10)}

    def _get_response(self, url, params=None, headers=None):
        if not headers:
            headers = _AbsDailyReader._headers
        if self.session:
            self.session.cookies = self._get_cookie('http://www.xueqiu.com')
        return super(_AbsDailyReader, self)._get_response(url, params, headers)

    def _read_lines(self, out):
        """加工原始数据"""
        df = pd.DataFrame(out['list'])
        df = df.rename(columns={'basiceps': '基本每股收益',
                                'epsdiluted': '每股收益(摊薄)',
                                'epsweighted': '每股收益(加权)',
                                'naps': '每股净资产',
                                'opercashpershare': '每股现金流',
                                'peropecashpershare': '每股经营性现金流',
                                'netassgrowrate': '净资产增长率(%)',
                                'dilutedroe': '净资产收益率(摊薄)(%)',
                                'weightedroe': '净资产收益率(加权)(%)',
                                'mainbusincgrowrate': '主营业务收入增长率(%)',
                                'netincgrowrate': '净利润增长率(%)',
                                'totassgrowrate': '总资产增长率(%)',
                                'salegrossprofitrto': '销售毛利率(%)',
                                'mainbusiincome': '主营业务收入',
                                'mainbusiprofit': '主营业务利润',
                                'totprofit': '利润总额',
                                'netprofit': '净利润',
                                'totalassets': '资产总额',
                                'totalliab': '负债总额',
                                'totsharequi': '股东权益合计',
                                'operrevenue': '经营活动产生的现金流量净额',
                                'invnetcashflow': '投资活动产生的现金流量净额',
                                'finnetcflow': '筹资活动产生的现金流量净额',
                                'chgexchgchgs': '汇率变动对现金及现金等价物的影响',
                                'cashnetr': '现金及现金等价物净增加额',
                                'cashequfinbal': '期末现金及现金等价物余额',
                                'symbol': '',
                                'name': '',
                                'totalshare': ''})
        df = df.drop(columns=['symbol', 'name', 'totalshare', 'compcode'])
        df['reportdate'] = pd.to_datetime(df['reportdate'], format='%Y%m%d')
        df = df.set_index('reportdate')
        return df
