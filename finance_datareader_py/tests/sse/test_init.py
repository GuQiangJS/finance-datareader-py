# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.sse import _download_sse_symbols, get_sse_symbols


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


if __name__ == '__main__':
    unittest.main()
