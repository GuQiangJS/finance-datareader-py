# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

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


if __name__ == '__main__':
    unittest.main()
