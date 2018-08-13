# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

import numpy as np

from finance_datareader_py.szse import _download_szse_symbols, get_szse_symbols


class sse_TestCase(unittest.TestCase):
    def test_download_szse_symbols(self):
        df1 = _download_szse_symbols('6')
        self.assertIsNotNone(df1)
        self.assertFalse(df1.empty)
        df2 = get_szse_symbols('6')
        self.assertIsNotNone(df2)
        self.assertFalse(df2.empty)
        self.assertTrue(df1.equals(df2))
        print(df1)

    def test_get_szse_symbols(self):
        df2 = get_szse_symbols('2')  # A股
        df5 = get_szse_symbols('5')  # 中小板
        df6 = get_szse_symbols('6')  # 创业板
        self.assertFalse(df2.empty)
        self.assertFalse(df5.empty)
        self.assertFalse(df6.empty)
        print(df2)
        print(df2.count())
        print(df5.count())
        print(df6.count())

        self.assertTrue(np.array_equal(
            df2[df2['symbol'].str.contains('^002', regex=True)].values,
            df5.values))
        self.assertTrue(np.array_equal(
            df2[df2['symbol'].str.contains('^3', regex=True)].values,
            df6.values))


if __name__ == '__main__':
    unittest.main()
