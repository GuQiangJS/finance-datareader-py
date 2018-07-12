# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

import numpy as np

from finance_datareader_py.sohu.daily import SohuDailyReader


class SohuDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = SohuDailyReader(symbols='000002').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

    def test_read_399300(self):
        """测试抓取沪深300指数数据

        :return:
        """
        df = SohuDailyReader(symbols='399300', prefix='zs_').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

    def test_read_column_dtype_is_numeric(self):
        df = SohuDailyReader(symbols='000002').read()
        for col_name in df.columns:
            self.assertEqual(df[col_name].dtype, np.float64)


if __name__ == '__main__':
    unittest.main()
