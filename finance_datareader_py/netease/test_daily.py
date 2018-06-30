# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

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
