# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json

import numpy as np
import pandas as pd

from finance_datareader_py import _AbsDailyReader

__all__ = ['EastMoneyDailyReader']


class EastMoneyDailyReader(_AbsDailyReader):
    """从 eastmoney 读取每日成交汇总数据（支持获取前复权、后复权的数据）

    Args:
        symbols: 股票代码。**此参数只接收单一股票代码**。For example:600001,000002
        type: {None, 'fa', 'ba' }, 默认值 None

            * None: 不复权（默认）
            * 'fa': 前复权
            * 'ba': 后复权

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
            type: {None, 'fa', 'ba'}, 默认值 None

                * None: 不复权（默认）
                * 'fa': 前复权
                * 'ba': 后复权

            start: 开始日期。默认值：2004-10-08
            end: 结束日期。默认值：当前日期的 **前一天** 。
            retry_count: 重试次数
            pause: 重试间隔时间
            session:
            chunksize:
        """
        super(EastMoneyDailyReader, self).__init__(symbols, start, end,
                                                   retry_count, pause, session,
                                                   chunksize)
        self._type = type

    @property
    def url(self):
        # http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id=0000022&type=k&authorityType=fa
        # http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id=6000001&type=k&authorityType=fa
        return 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js'

    def _parse_symbol(self):
        # 深市后加2，沪市后加1
        return self.symbols + ('1' if self.symbols[0] == '6' else '2')

    def _get_params(self, *args, **kwargs):
        return {'rtntype': '5', 'id': self._parse_symbol(), 'type': 'k',
                'authorityType': self._type if self._type else ''}

    def read(self):
        """读取数据

        Returns:
            ``pandas.DataFrame``:

            无数据时返回空白的 ``pandas.DataFrame`` 。参见 ``pandas.DataFrame.empty``。

        Examples:
            .. testcode:: python

                from finance_datareader_py.eastmoney.daily import EastMoneyDailyReader

                df = EastMoneyDailyReader(symbols='000002').read()
                # 前复权
                # df = EastMoneyDailyReader(symbols='000002', type='fa').read()
                # 后复权
                # df = EastMoneyDailyReader(symbols='000002', type='ba').read()

                print(df)

            .. testoutput::

                   日期    Open  Close   High    Low  交易量(手)   成交金额     振幅   换手率
                2004-10-08   5.42   5.56   5.60   5.28  117073  6369万   5.9%  0.74
                2004-10-11   5.56   5.54   5.65   5.51  264020  1.48亿  2.52%  1.67
                2004-10-12   5.53   5.79   5.87   5.50  600868  3.46亿  6.68%  3.81
                ...           ...    ...    ...    ...     ...    ...    ...   ...
                2018-07-03  23.10  23.42  23.48  22.80  549965  12.7亿  2.98%  0.57
                2018-07-04  23.46  23.00  23.75  23.00  249881  5.82亿   3.2%  0.26
                2018-07-05  23.02  23.05  23.41  22.85  267279  6.19亿  2.43%  0.28

        """
        try:
            return super(EastMoneyDailyReader, self).read()
        finally:
            self.close()

    def _read_url_as_StringIO(self, url, params=None):
        """读取原始数据"""
        response = self._get_response(url, params=params)
        txt = EastMoneyDailyReader._get_split_txt(response.text)
        if not txt:
            return pd.DataFrame()
        pd_data = pd.DataFrame([f.split(',') for f in json.loads(txt)])
        return pd_data

    def _get_split_txt(txt):
        """自动截取文本中的每日数据。（区分前复权、后复权、不复权）"""
        s_txts = ['"data":']
        e_txt = ']'
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
                     5: '交易量(手)', 6: '成交金额', 7: '振幅(%)', 8: '换手率'},
            inplace=True)
        if 6 in out:
            out.drop([6], axis=1, inplace=True)
        out = out.replace('-', np.nan).replace('None', np.nan)
        # 转换 Date 列为 datetime 数据类型
        out['日期'] = pd.to_datetime(out['日期'])
        # out['涨跌幅'] = out['涨跌幅'].str.replace('%', '')
        # out['换手率'] = out['换手率'].str.replace('%', '')
        # 将 Date 列设为索引列
        out['振幅(%)'] = out['振幅(%)'].str.replace('%', '')
        out.set_index("日期", inplace=True)
        out = self._convert_numeric_allcolumns(out)
        return out[self.start:self.end]
