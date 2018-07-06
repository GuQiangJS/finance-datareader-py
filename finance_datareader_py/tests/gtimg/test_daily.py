# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import unittest

from finance_datareader_py.gtimg.daily import GtimgDailyReader


class GtimgDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = GtimgDailyReader(symbols='000002').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)
        # df = GtimgDailyReader(symbols='000002', type='hfq').read()
        # print(df)
        # df = GtimgDailyReader(symbols='000002', type='qfq').read()
        # print(df)

    def test_read_399330(self):
        """测试抓取沪深300指数数据

        :return:
        """
        df = GtimgDailyReader(symbols='399300',
                              start=datetime.date(2002, 1, 4)).read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

    def test_read_err_symbol(self):
        """测试读取错误的股票代码

        Returns:

        """
        df = GtimgDailyReader(symbols='123').read()
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)


if __name__ == '__main__':
    unittest.main()
