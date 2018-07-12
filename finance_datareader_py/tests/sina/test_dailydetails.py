# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import unittest

import numpy as np
import requests

from finance_datareader_py import _AbsDailyReader
from finance_datareader_py.sina.daily_details import SinaDailyDetailsReader


class SinaDailyDetailsReader_TestCase(unittest.TestCase):
    def setUp(self):
        # response.status_code==456 表示当前IP被新浪临时封禁。
        # 这样后面的测试也就不需要再继续下去了
        rep = requests.get('http://market.finance.sina.com.cn/downxls.php?date\
            =2018-07-03&symbol=sz000002', headers=_AbsDailyReader._headers)
        self._enable = rep.status_code != 456

    def test_read_single(self):
        if not self._enable:
            return
        df = SinaDailyDetailsReader(symbols='000002',
                                    start=datetime.date(2018, 7, 2),
                                    end=datetime.date(2018, 7, 2)).read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

        # 测试数据
        ft = '%Y-%m-%d %H:%M:%S'
        d = {
            '2018-07-02 09:25:03': {
                '成交价': np.float64(24.5),
                '价格变动': np.float64(24.5),
                '成交量(手)': np.float64(871),
                '成交额(元)': np.float64(2133950),
                '性质': '买盘'
            },
            '2018-07-02 09:30:00': {
                '成交价': np.float64(24.5),
                '价格变动': np.float64(0),
                '成交量(手)': np.float64(0),
                '成交额(元)': np.float64(0),
                '性质': '买盘'
            },
            '2018-07-02 14:57:00': {
                '成交价': np.float64(22.79),
                '价格变动': np.float64(0),
                '成交量(手)': np.float64(9),
                '成交额(元)': np.float64(20511),
                '性质': '卖盘'
            },
            '2018-07-02 15:00:03': {
                '成交价': np.float64(22.80),
                '价格变动': np.float64(0.01),
                '成交量(手)': np.float64(5763),
                '成交额(元)': np.float64(13139640),
                '性质': '买盘'
            }
        }
        # 测试数据

        for k, v in d.items():
            dt = datetime.datetime.strptime(k, ft)
            for name, value in v.items():
                v = df.loc[dt, name]
                self.assertEqual(value, v)

    def test_read_mulit(self):
        if not self._enable:
            return
        start = datetime.date(2018, 6, 25)
        end = datetime.date(2018, 7, 2)

        df = SinaDailyDetailsReader(symbols='000002', start=start,
                                    end=end).read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

        while start <= end:
            if not start.weekday():
                df_1 = SinaDailyDetailsReader(symbols='000002', start=start,
                                              end=start).read()
                df_2 = df[start.strftime('%Y-%m-%d')]
                self.assertTrue(df_1.equals(df_2))
            start = start + datetime.timedelta(days=1)

    def test_read_err_symbol(self):
        """测试读取错误的股票代码

        Returns:

        """
        if not self._enable:
            return
        df = SinaDailyDetailsReader(symbols='123',
                                    start=datetime.date(2018, 7, 2),
                                    end=datetime.date(2018, 7, 2)).read()
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)

    def test_read_column_dtype_is_numeric(self):
        if not self._enable:
            return
        df = SinaDailyDetailsReader(symbols='399300').read()
        for col_name in '成交价格', '价格变动', '成交量(手)', '成交额(元)':
            self.assertEqual(df[col_name].dtype, np.float64)


if __name__ == '__main__':
    unittest.main()
