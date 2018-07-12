# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import unittest

import numpy as np

from finance_datareader_py.netease.daily import NetEaseDailyReader


class NetEaseDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = NetEaseDailyReader(symbols='000002').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

    def test_read_399330(self):
        """测试抓取沪深300指数数据

        :return:
        """
        df = NetEaseDailyReader(symbols='399300',
                                start=datetime.date(2002, 1, 4)).read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

    def test_read_err_symbol(self):
        """测试读取错误的股票代码

        Returns:

        """
        df = NetEaseDailyReader(symbols='123').read()
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)

    def test_read_column_dtype_is_numeric(self):
        df = NetEaseDailyReader(symbols='399300').read()
        for col_name in df.columns:
            self.assertEqual(df[col_name].dtype, np.float64)


if __name__ == '__main__':
    unittest.main()
