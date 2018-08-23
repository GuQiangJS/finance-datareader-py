# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>


__all__ = ['daily', 'FinancialIndicatorReader']

import pandas as pd

from finance_datareader_py import _AbsDailyReader


def _parse_symbol(prefix: str, symbol: str):
    if not prefix or not symbol:
        raise ValueError()
    return prefix + symbol


class FinancialIndicatorReader(_AbsDailyReader):
    """从 Sohu 读取主要财务指标

    **从1990-01-01开始获取数据**。

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:

    Returns:
        ``DataFrame``: 结果按照 公告日期 **倒序** 排序。 任意数据表无数据时返回 空白的
        ``pandas.DataFrame`` 。 参见 ``pandas.DataFrame.empty``。

        输出列集合：
        .. code-block:: json

            [
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

            >>> from finance_datareader_py.sohu import FinancialIndicatorReader

            >>> df = FinancialIndicatorReader('601398').read()
    """

    def __init__(self, symbols=None, retry_count=3, pause=1, session=None,
                 chunksize=25):
        """从 Sohu 读取主要财务指标

        **从1990-01-01开始获取数据**。

        Args:
            symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002,300002
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:

        Returns:
            ``DataFrame``: 结果按照 公告日期 **倒序** 排序。 任意数据表无数据时返回 空白的
            ``pandas.DataFrame`` 。 参见 ``pandas.DataFrame.empty``。

            输出列集合：
            .. code-block:: json

                [
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

                >>> from finance_datareader_py.sohu import FinancialIndicatorReader

                >>> df = FinancialIndicatorReader('601398').read()
        """
        super(FinancialIndicatorReader, self).__init__(symbols, None, None,
                                                       retry_count, pause,
                                                       session,
                                                       chunksize)
        self._encoding = 'gb2312'

    @property
    def url(self):
        # http://quotes.money.163.com/service/zycwzb_300104.html?type=report
        return 'http://quotes.money.163.com/service/zycwzb_{' \
               '0}.html?type=report'.format(self.symbols)

    def _get_params(self, *args, **kwargs):
        return ''

    def read(self):
        df = super(FinancialIndicatorReader, self).read()
        df = df.transpose().dropna(how='all')
        df.index = pd.to_datetime(df.index)
        return df
