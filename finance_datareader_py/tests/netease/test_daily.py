# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.netease.daily import NetEaseDailyReader


class NetEaseDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = NetEaseDailyReader(symbols='000002').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)


if __name__ == '__main__':
    unittest.main()
