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

        输出列集合：
        .. code-block:: json

            [
                "总资产增长率(%)",
                "净资产增长率(%)",
                "净利润增长率(%)",
                "主营业务收入增长率(%)",
                "现金流量比率(%)",
                "经营现金净流量对负债比率(%)",
                "经营现金净流量与净利润的比率(%)",
                "资产的经营现金流量回报率(%)",
                "经营现金净流量对销售收入比率(%)",
                "流动资产周转天数(天)",
                "流动资产周转率(次)",
                "总资产周转天数(天)",
                "存货周转天数(天)",
                "总资产周转率(次)",
                "固定资产周转率(次)",
                "存货周转率(次)",
                "应收账款周转天数(天)",
                "应收账款周转率(次)",
                "固定资产比重(%)",
                "清算价值比率(%)",
                "产权比率(%)",
                "资本固定化比率(%)",
                "固定资产净值率(%)",
                "资本化比率(%)",
                "长期资产与长期资金比率(%)",
                "负债与所有者权益比率(%)",
                "股东权益与固定资产比率(%)",
                "长期负债比率(%)",
                "股东权益比率(%)",
                "长期债务与营运资金比率(%)",
                "资产负债率(%)",
                "利息支付倍数(%)",
                "现金比率(%)",
                "速动比率(%)",
                "流动比率(%)",
                "主营利润比重(%)",
                "非主营比重(%)",
                "三项费用比重(%)",
                "销售毛利率(%)",
                "资产报酬率(%)",
                "净资产报酬率(%)",
                "股本报酬率(%)",
                "净资产收益率(%)",
                "销售净利率(%)",
                "主营业务成本率(%)",
                "营业利润率(%)",
                "成本费用利润率(%)",
                "总资产净利润率(%)",
                "主营业务利润率(%)",
                "总资产利润率(%)",
                "净资产收益率加权(%)",
                "股东权益不含少数股东权益(万元)",
                "流动负债(万元)",
                "总负债(万元)",
                "流动资产(万元)",
                "总资产(万元)",
                "现金及现金等价物净增加额(万元)",
                "经营活动产生的现金流量净额(万元)",
                "净利润(扣除非经常性损益后)(万元)",
                "净利润(万元)",
                "利润总额(万元)",
                "营业外收支净额(万元)",
                "投资收益(万元)",
                "营业利润(万元)",
                "主营业务利润(万元)",
                "主营业务收入(万元)",
                "每股经营活动产生的现金流量净额(元)",
                "每股净资产(元)",
                "基本每股收益(元)"
            ]

    Examples:
        .. code-block:: python

            >>> from finance_datareader_py.netease import FinancialIndicatorReader
            >>> df = FinancialIndicatorReader('601398').read()
            >>> print(df.loc[df.index[-1],['基本每股收益(元)','每股净资产(元)']])

            基本每股收益(元)    0.22
            每股净资产(元)     5.85
            Name: 2018-03-31 00:00:00, dtype: object
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

            输出列集合：
            .. code-block:: json

                [
                    "总资产增长率(%)",
                    "净资产增长率(%)",
                    "净利润增长率(%)",
                    "主营业务收入增长率(%)",
                    "现金流量比率(%)",
                    "经营现金净流量对负债比率(%)",
                    "经营现金净流量与净利润的比率(%)",
                    "资产的经营现金流量回报率(%)",
                    "经营现金净流量对销售收入比率(%)",
                    "流动资产周转天数(天)",
                    "流动资产周转率(次)",
                    "总资产周转天数(天)",
                    "存货周转天数(天)",
                    "总资产周转率(次)",
                    "固定资产周转率(次)",
                    "存货周转率(次)",
                    "应收账款周转天数(天)",
                    "应收账款周转率(次)",
                    "固定资产比重(%)",
                    "清算价值比率(%)",
                    "产权比率(%)",
                    "资本固定化比率(%)",
                    "固定资产净值率(%)",
                    "资本化比率(%)",
                    "长期资产与长期资金比率(%)",
                    "负债与所有者权益比率(%)",
                    "股东权益与固定资产比率(%)",
                    "长期负债比率(%)",
                    "股东权益比率(%)",
                    "长期债务与营运资金比率(%)",
                    "资产负债率(%)",
                    "利息支付倍数(%)",
                    "现金比率(%)",
                    "速动比率(%)",
                    "流动比率(%)",
                    "主营利润比重(%)",
                    "非主营比重(%)",
                    "三项费用比重(%)",
                    "销售毛利率(%)",
                    "资产报酬率(%)",
                    "净资产报酬率(%)",
                    "股本报酬率(%)",
                    "净资产收益率(%)",
                    "销售净利率(%)",
                    "主营业务成本率(%)",
                    "营业利润率(%)",
                    "成本费用利润率(%)",
                    "总资产净利润率(%)",
                    "主营业务利润率(%)",
                    "总资产利润率(%)",
                    "净资产收益率加权(%)",
                    "股东权益不含少数股东权益(万元)",
                    "流动负债(万元)",
                    "总负债(万元)",
                    "流动资产(万元)",
                    "总资产(万元)",
                    "现金及现金等价物净增加额(万元)",
                    "经营活动产生的现金流量净额(万元)",
                    "净利润(扣除非经常性损益后)(万元)",
                    "净利润(万元)",
                    "利润总额(万元)",
                    "营业外收支净额(万元)",
                    "投资收益(万元)",
                    "营业利润(万元)",
                    "主营业务利润(万元)",
                    "主营业务收入(万元)",
                    "每股经营活动产生的现金流量净额(元)",
                    "每股净资产(元)",
                    "基本每股收益(元)"
                ]

        Examples:
            .. code-block:: python

                >>> from finance_datareader_py.netease import FinancialIndicatorReader
                >>> df = FinancialIndicatorReader('601398').read()
                >>> print(df.loc[df.index[-1],['基本每股收益(元)','每股净资产(元)']])

                基本每股收益(元)    0.22
                每股净资产(元)     5.85
                Name: 2018-03-31 00:00:00, dtype: object
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
