# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.sse import _download_sse_symbols, get_sse_symbols
from finance_datareader_py.sse import get_dividends


class sse_TestCase(unittest.TestCase):
    def test_download_sse_symbols(self):
        df1 = _download_sse_symbols(30)
        self.assertIsNotNone(df1)
        self.assertFalse(df1.empty)
        df2 = get_sse_symbols()
        self.assertIsNotNone(df2)
        self.assertFalse(df2.empty)
        self.assertTrue(df1.equals(df2))
        print(df2)

    def test_get_sse_dividends(self):
        df1, df2 = get_dividends('600006')
        self.assertIsNotNone(df1)
        self.assertFalse(df1.empty)
        self.assertIsNotNone(df2)
        self.assertFalse(df2.empty)
        print(df1)
        print(df2)

    def test_get_sse_dividends_err1(self):
        """测试传入的股票代码不正确时，是否抛出异常"""
        self.assertRaises(ValueError, get_dividends, '300001')
        self.assertRaises(ValueError, get_dividends, '000001')
        self.assertRaises(ValueError, get_dividends, '')


if __name__ == '__main__':
    unittest.main()
