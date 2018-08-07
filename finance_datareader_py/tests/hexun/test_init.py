# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest
from finance_datareader_py.hexun import get_deposit_interest_rate


class hexun_TestCase(unittest.TestCase):
    def test_get_deposit_interest_rate(self):
        d = get_deposit_interest_rate()
        self.assertTrue(d)
        print(d)


if __name__ == '__main__':
    unittest.main()
