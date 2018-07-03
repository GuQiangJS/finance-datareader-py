# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import unittest

import numpy as np
import pandas as pd

from finance_datareader_py.sina import get_dividends


class sina_TestCase(unittest.TestCase):
    def test_get_dividends(self):
        df1, df2 = get_dividends('000541')
        self.assertIsNotNone(df1)
        self.assertFalse(df1.empty)
        self.assertIsNotNone(df2)
        self.assertFalse(df2.empty)
        print(df1)
        print(df2)

        dt = datetime.date(2018, 5, 5)
        self.assertEqual(np.float32(3.29), df1.loc[dt, '派息(税前)(元)'])
        self.assertTrue(pd.isna(df1.loc[dt, '红股上市日']))
        self.assertEqual(pd.Timestamp(2018, 5, 10), df1.loc[dt, '股权登记日'])
        self.assertEqual(np.float32(1), df1.loc[dt, '转增(股)'])
        self.assertEqual(np.float32(0), df1.loc[dt, '送股(股)'])
        self.assertEqual(pd.Timestamp(2018, 5, 11), df1.loc[dt, '除权除息日'])

        dt = datetime.date(1994, 12, 24)
        self.assertEqual(np.float32(2), df2.loc[dt, '配股方案(每10股配股股数)'])
        self.assertEqual(np.float32(8), df2.loc[dt, '配股价格(元)'])
        self.assertEqual(np.float32(115755000), df2.loc[dt, '基准股本(万股)'])
        self.assertEqual(pd.Timestamp(1995, 1, 4), df2.loc[dt, '除权日'])
        self.assertEqual(pd.Timestamp(1995, 1, 3), df2.loc[dt, '股权登记日'])
        self.assertEqual(pd.Timestamp(1995, 1, 16), df2.loc[dt, '缴款起始日'])
        self.assertEqual(pd.Timestamp(1995, 1, 27), df2.loc[dt, '缴款终止日'])
        self.assertEqual(pd.Timestamp(1995, 2, 22), df2.loc[dt, '配股上市日'])
        self.assertTrue(pd.isna(df2.loc[dt, '募集资金合计(元)']))


if __name__ == '__main__':
    unittest.main()
