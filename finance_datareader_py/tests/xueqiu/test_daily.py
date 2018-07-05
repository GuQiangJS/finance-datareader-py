# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import unittest

from finance_datareader_py.xueqiu.daily import XueQiuDailyReader


class XueQiuDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = XueQiuDailyReader(symbols='000002', start=datetime.date(
            2010, 1, 1)).read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)

    def test_read_all(self):
        y = datetime.datetime.today() + datetime.timedelta(days=-10)
        for i in ['default', 'before', 'after']:
            df = XueQiuDailyReader(symbols='000002', type=i, start=y).read()
            self.assertIsNotNone(df)
            self.assertFalse(df.empty)
            print(df)
            print('-----------------------------------------------')

    def test_read_err(self):
        df = XueQiuDailyReader(symbols='600001', start=datetime.date(
            2010, 1, 1)).read()
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)
        print(df)


if __name__ == '__main__':
    unittest.main()
