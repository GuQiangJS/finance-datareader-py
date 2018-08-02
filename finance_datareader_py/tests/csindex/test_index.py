# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest
from finance_datareader_py.csindex import get_stock_holdings


class csindex_TestCase(unittest.TestCase):
    def test_get_stock_holdings(self):
        df = get_stock_holdings('000300')
        self.assertFalse(df.empty)
        self.assertEqual(300, len(df.index))
        print(df)

    def test_get_stock_holdings(self):
        self.assertRaises(ValueError, get_stock_holdings, '')
        self.assertRaises(ValueError, get_stock_holdings, None)

if __name__ == '__main__':
    unittest.main()
