# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

import numpy as np

from finance_datareader_py.eastmoney.daily import EastMoneyDailyReader


class EastMoneyDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = EastMoneyDailyReader(symbols='000002').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)
        # df = EastMoneyDailyReader(symbols='000002', type='fa').read()
        # print(df)
        # df = EastMoneyDailyReader(symbols='000002', type='ba').read()
        # print(df)

    def test_read_err_symbol(self):
        """测试读取错误的股票代码"""
        df = EastMoneyDailyReader(symbols='123').read()
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)

    def test_read_column_dtype_is_numeric(self):
        df = EastMoneyDailyReader(symbols='000002').read()
        ss = 'Open', 'Close', 'High', 'Low', '交易量(手)', '换手率', '振幅(%)'
        for s in ss:
            self.assertEqual(df[s].dtype, np.float64)


if __name__ == '__main__':
    unittest.main()
