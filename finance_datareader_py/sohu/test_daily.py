# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.sohu.daily import SohuDailyReader


class SohuDailyReader_TestCase(unittest.TestCase):
    def test_read(self):
        df = SohuDailyReader(symbols='000002').read()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        print(df)


if __name__ == '__main__':
    unittest.main()
