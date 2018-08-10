# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.csindex import get_stock_holdings
from finance_datareader_py.csindex import get_stock_holdings_weight


class csindex_TestCase(unittest.TestCase):
    def test_get_stock_holdings(self):
        df = get_stock_holdings('000300')
        self.assertFalse(df.empty)
        self.assertEqual(300, len(df.index))
        print(df)

    def test_get_stock_holdings_ValueError(self):
        self.assertRaises(ValueError, get_stock_holdings, '')
        self.assertRaises(ValueError, get_stock_holdings, None)

    def test_get_stock_holdings_weight(self):
        df = get_stock_holdings_weight('000300')
        self.assertFalse(df.empty)
        self.assertEqual(300, len(df.index))
        print(df)
        self.assertEqual(df.dtypes[0], 'object')
        self.assertEqual(df.dtypes[1], 'object')
        self.assertEqual(df.dtypes[2], 'float32')

    def test_get_stock_holdings_weight_ValueError(self):
        self.assertRaises(ValueError, get_stock_holdings_weight, '')
        self.assertRaises(ValueError, get_stock_holdings_weight, None)


if __name__ == '__main__':
    unittest.main()
