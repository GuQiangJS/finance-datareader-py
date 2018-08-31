# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import unittest

import numpy as np
import pandas as pd

from finance_datareader_py.sina import SinaQuoteReader
from finance_datareader_py.sina import get_cpi
from finance_datareader_py.sina import get_dividends
from finance_datareader_py.sina import get_measure_of_money_supply


class sina_TestCase(unittest.TestCase):
    def test_get_dividends(self):
        df1, df2 = get_dividends('000541')
        self.assertIsNotNone(df1)
        self.assertFalse(df1.empty)
        self.assertIsNotNone(df2)
        self.assertFalse(df2.empty)
        print(df1)
        print('------------')
        print(df2)

        dt = datetime.date(2018, 5, 5)
        df1 = df1.loc[df1['公告日期'] == dt]
        self.assertEqual(np.float64(3.29), df1.at[0, '派息(税前)(元)'])
        self.assertTrue(pd.isna(df1.at[0, '红股上市日']))
        self.assertEqual(pd.Timestamp(2018, 5, 10), df1.at[0, '股权登记日'])
        self.assertEqual(np.float64(1), df1.at[0, '转增(股)'])
        self.assertEqual(np.float64(0), df1.at[0, '送股(股)'])
        self.assertEqual(pd.Timestamp(2018, 5, 11), df1.at[0, '除权除息日'])

        dt = datetime.date(1994, 12, 24)
        df2 = df2.loc[df2['公告日期'] == dt]
        self.assertEqual(np.float64(2), df2.at[0, '配股方案(每10股配股股数)'])
        self.assertEqual(np.float64(8), df2.at[0, '配股价格(元)'])
        self.assertEqual(np.float64(115755000), df2.at[0, '基准股本(万股)'])
        self.assertEqual(pd.Timestamp(1995, 1, 4), df2.at[0, '除权日'])
        self.assertEqual(pd.Timestamp(1995, 1, 3), df2.at[0, '股权登记日'])
        self.assertEqual(pd.Timestamp(1995, 1, 16), df2.at[0, '缴款起始日'])
        self.assertEqual(pd.Timestamp(1995, 1, 27), df2.at[0, '缴款终止日'])
        self.assertEqual(pd.Timestamp(1995, 2, 22), df2.at[0, '配股上市日'])
        self.assertTrue(pd.isna(df2.at[0, '募集资金合计(元)']))

    def test_read_err_symbol(self):
        """测试读取错误的股票代码"""
        df1, df2 = get_dividends('123')
        self.assertIsNotNone(df1)
        self.assertTrue(df1.empty)
        self.assertIsNotNone(df2)
        self.assertTrue(df2.empty)

    def test_read_fh(self):
        """测试读取只有分红没有配股数据"""
        df1, df2 = get_dividends('300378')
        self.assertIsNotNone(df1)
        self.assertFalse(df1.empty)
        print(df1)
        self.assertIsNotNone(df2)
        self.assertTrue(df2.empty)

    def test_read_column_dtype(self):
        df1, df2 = get_dividends(symbol='000541')

        for df in df1, df2:
            for col_name in df.columns:
                if '日' in col_name:
                    self.assertEqual(df[col_name].dtype, 'datetime64[ns]',
                                     msg=col_name)
                else:
                    self.assertEqual(df[col_name].dtype, np.float64,
                                     msg=col_name)

    def test_get_cpi(self):
        df = get_cpi()
        print(df.tail())
        print(df)
        c = (datetime.date.today().year - 1 - 1990) * 12 + \
            datetime.date.today().month
        print('{0}>{1}'.format(len(df.index), c))
        self.assertTrue(len(df.index) > c)
        self.assertFalse(df.empty)
        for i in range(2016, 2017):
            for j in range(1, 12):
                v = df.loc['{0}.{1}'.format(i, j)]['价格指数']
                self.assertIsInstance(v, np.float64)
                self.assertTrue(v)
                print(v)

    def test_get_measure_of_money_supply(self):
        df = get_measure_of_money_supply()
        print(df.iloc[0][df.columns[0]])
        print(df.columns)
        print(df.index[-1])
        c = (datetime.date.today().year - 1 - 1978) * 12 + \
            datetime.date.today().month
        print('{0}>{1}'.format(len(df.index), c))
        self.assertFalse(df.empty)


class SinaQuoteReader_TestCase(unittest.TestCase):
    def test_read_single(self):
        reader = SinaQuoteReader('000002')
        try:
            df = reader.read()
            self.assertIsNotNone(df)
            self.assertFalse(df.empty)
            print(df)
        finally:
            reader.close()

    def test_read_mulit(self):
        lst = ('000002', '300027', '000927')
        reader = SinaQuoteReader(lst)
        try:
            p = reader.read()
            self.assertIsNotNone(p)
            for s in lst:
                self.assertTrue(s in p['price'])
                self.assertTrue(s in p['datetime'])
                print('{:8}{:>7} {}.'.format(s, p['price'][s][0],
                                             p['datetime'][s][0]))
        finally:
            reader.close()


if __name__ == '__main__':
    unittest.main()
