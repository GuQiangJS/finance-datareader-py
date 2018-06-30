# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import unittest

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
        print(df2.count())
        print(df5.count())
        print(df6.count())
        self.assertTrue(df2.filter(regex='^002', axis=0).equals(df5))
        self.assertTrue(df2.filter(regex='^3', axis=0).equals(df6))


if __name__ == '__main__':
    unittest.main()
