# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

__all__ = ['daily']

import numpy as np
import pandas as pd

from finance_datareader_py import _AbsDailyReader


class FinancialIndicatorReader(_AbsDailyReader):
    """从 网易 读取主要财务指标

    **从1990-01-01开始获取数据**。

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:

    Returns:
        ``DataFrame``: 结果按照 公告日期 **正序** 排序。 任意数据表无数据时返回 空白的
        ``pandas.DataFrame`` 。 参见 ``pandas.DataFrame.empty``。

    Examples:
        .. code-block:: python

            >>> from finance_datareader_py.netease import FinancialIndicatorReader
            >>> df = FinancialIndicatorReader('601398').read()
            >>> print(df.iloc[-1][:-1])

            总资产增长率(%)                   6.38
            净资产增长率(%)                   6.84
            净利润增长率(%)                      4
            主营业务收入增长率(%)                 NaN
            现金流量比率(%)                    NaN
            经营现金净流量对负债比率(%)                0
            经营现金净流量与净利润的比率(%)           0.79
            资产的经营现金流量回报率(%)                0
            经营现金净流量对销售收入比率(%)            NaN
            流动资产周转天数(天)                  NaN
            流动资产周转率(次)                   NaN
            总资产周转天数(天)                   NaN
            存货周转天数(天)                    NaN
            总资产周转率(次)                    NaN
            固定资产周转率(次)                   NaN
            存货周转率(次)                     NaN
            应收账款周转天数(天)                  NaN
            应收账款周转率(次)                   NaN
            固定资产比重(%)                    NaN
            清算价值比率(%)                    NaN
            产权比率(%)                        0
            资本固定化比率(%)               1212.58
            固定资产净值率(%)                   NaN
            资本化比率(%)                     NaN
            长期资产与长期资金比率(%)               NaN
            负债与所有者权益比率(%)            1112.58
            股东权益与固定资产比率(%)               NaN
            长期负债比率(%)                    NaN
            股东权益比率(%)                   8.25
            长期债务与营运资金比率(%)               NaN
                                     ...
            销售毛利率(%)                   50.86
            资产报酬率(%)                     0.3
            净资产报酬率(%)                   3.62
            股本报酬率(%)                   22.19
            净资产收益率(%)                   3.63
            销售净利率(%)                     NaN
            主营业务成本率(%)                   NaN
            营业利润率(%)                     NaN
            成本费用利润率(%)                255.18
            总资产净利润率(%)                   0.3
            主营业务利润率(%)                   NaN
            总资产利润率(%)                    0.3
            净资产收益率加权(%)                 3.85
            股东权益不含少数股东权益(万元)       217151000
            流动负债(万元)                     NaN
            总负债(万元)               2430887600
            流动资产(万元)                     NaN
            总资产(万元)               2649378100
            现金及现金等价物净增加额(万元)             NaN
            经营活动产生的现金流量净额(万元)        6216000
            净利润(扣除非经常性损益后)(万元)       7779500
            净利润(万元)                  7880200
            利润总额(万元)                10164600
            营业外收支净额(万元)               136000
            投资收益(万元)                  267800
            营业利润(万元)                10028600
            主营业务利润(万元)              10028600
            主营业务收入(万元)              19719800
            每股经营活动产生的现金流量净额(元)           NaN
            每股净资产(元)                    5.85
            Name: 2018-03-31 00:00:00, Length: 68, dtype: object

    """

    def __init__(self, symbols=None, retry_count=3, pause=1, session=None,
                 chunksize=25):
        """从 网易 读取主要财务指标

        **从1990-01-01开始获取数据**。

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:

        Returns:
            ``DataFrame``: 结果按照 公告日期 **正序** 排序。 任意数据表无数据时返回 空白的
            ``pandas.DataFrame`` 。 参见 ``pandas.DataFrame.empty``。

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.netease import FinancialIndicatorReader
                >>> df = FinancialIndicatorReader('601398').read()
                >>> print(df.iloc[-1][:-1])

                总资产增长率(%)                   6.38
                净资产增长率(%)                   6.84
                净利润增长率(%)                      4
                主营业务收入增长率(%)                 NaN
                现金流量比率(%)                    NaN
                经营现金净流量对负债比率(%)                0
                经营现金净流量与净利润的比率(%)           0.79
                资产的经营现金流量回报率(%)                0
                经营现金净流量对销售收入比率(%)            NaN
                流动资产周转天数(天)                  NaN
                流动资产周转率(次)                   NaN
                总资产周转天数(天)                   NaN
                存货周转天数(天)                    NaN
                总资产周转率(次)                    NaN
                固定资产周转率(次)                   NaN
                存货周转率(次)                     NaN
                应收账款周转天数(天)                  NaN
                应收账款周转率(次)                   NaN
                固定资产比重(%)                    NaN
                清算价值比率(%)                    NaN
                产权比率(%)                        0
                资本固定化比率(%)               1212.58
                固定资产净值率(%)                   NaN
                资本化比率(%)                     NaN
                长期资产与长期资金比率(%)               NaN
                负债与所有者权益比率(%)            1112.58
                股东权益与固定资产比率(%)               NaN
                长期负债比率(%)                    NaN
                股东权益比率(%)                   8.25
                长期债务与营运资金比率(%)               NaN
                                         ...
                销售毛利率(%)                   50.86
                资产报酬率(%)                     0.3
                净资产报酬率(%)                   3.62
                股本报酬率(%)                   22.19
                净资产收益率(%)                   3.63
                销售净利率(%)                     NaN
                主营业务成本率(%)                   NaN
                营业利润率(%)                     NaN
                成本费用利润率(%)                255.18
                总资产净利润率(%)                   0.3
                主营业务利润率(%)                   NaN
                总资产利润率(%)                    0.3
                净资产收益率加权(%)                 3.85
                股东权益不含少数股东权益(万元)       217151000
                流动负债(万元)                     NaN
                总负债(万元)               2430887600
                流动资产(万元)                     NaN
                总资产(万元)               2649378100
                现金及现金等价物净增加额(万元)             NaN
                经营活动产生的现金流量净额(万元)        6216000
                净利润(扣除非经常性损益后)(万元)       7779500
                净利润(万元)                  7880200
                利润总额(万元)                10164600
                营业外收支净额(万元)               136000
                投资收益(万元)                  267800
                营业利润(万元)                10028600
                主营业务利润(万元)              10028600
                主营业务收入(万元)              19719800
                每股经营活动产生的现金流量净额(元)           NaN
                每股净资产(元)                    5.85
                Name: 2018-03-31 00:00:00, Length: 68, dtype: object
        """
        super(FinancialIndicatorReader, self).__init__(symbols, None, None,
                                                       retry_count, pause,
                                                       session,
                                                       chunksize)
        self._encoding = 'gb2312'

    @property
    def url(self):
        # 成长能力 http://quotes.money.163.com/service/zycwzb_603105.html?type=report&part=cznl
        # 营运能力 http://quotes.money.163.com/service/zycwzb_603105.html?type=report&part=yynl
        # 偿还能力 http://quotes.money.163.com/service/zycwzb_603105.html?type=report&part=chnl
        # 盈利能力 http://quotes.money.163.com/service/zycwzb_603105.html?type=report&part=ylnl
        # 主要财务指标 http://quotes.money.163.com/service/zycwzb_603105.html?type=report
        # return 'http://quotes.money.163.com/service/zycwzb_{' \
        #        '0}.html?type=report'.format(self.symbols)
        return 'http://quotes.money.163.com/service/zycwzb_{0}.html'.format(
            self.symbols)

    def _get_params(self, *args, **kwargs):
        return ''

    def read(self):
        d = ('cznl', 'yynl', 'chnl', 'ylnl', '')
        df = pd.DataFrame()
        for dd in d:
            df = df.join(self._read_single(self.url, {'type': 'report',
                                                      'part': dd}),
                         how='outer')
        return df

    def _read_single(self, url, params):
        df = self._read_one_data(url, params=params)
        df = df.transpose().dropna(how='all')
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df.replace(r'[^0-9\.]', np.NaN, regex=True)
        df = df.dropna(how='all')
        return df
