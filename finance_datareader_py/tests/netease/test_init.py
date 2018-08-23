# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

import pandas as pd

from finance_datareader_py.netease import FinancialIndicatorReader


class FinancialIndicatorReader_TestCase(unittest.TestCase):
    def test_FinancialIndicatorReader(self):
        df = FinancialIndicatorReader('601398').read()
        self.assertFalse(df.empty)
        print(df.tail())
        print(df.columns)
        dr = pd.date_range('2017-01-31', '2017-12-31', freq='M')
        df_2017 = pd.DataFrame(df, index=dr).dropna(how='all')
        self.assertFalse(df_2017.empty)
        self.assertEqual(len(df_2017.index), 4)
        print(df.iloc[-1][:-1])


if __name__ == '__main__':
    unittest.main()
