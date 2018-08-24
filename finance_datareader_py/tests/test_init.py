# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py import DailyReader


class DailyReaderTestCase(unittest.TestCase):
    def test_read(self):
        code = '601398'
        df = DailyReader(code).read()
        self.assertFalse(df.empty)
        print(df.tail())
        df_1 = DailyReader(int(code)).read()
        self.assertFalse(df_1.empty)
        print(df_1.tail())
        self.assertEqual(df.index.size, df_1.index.size)
        self.assertTrue(df.index.equals(df_1.index))
        df_2 = DailyReader([code]).read()
        self.assertFalse(df_2.empty)
        print(df_2.tail())
        self.assertEqual(df.index.size, df_2.index.size)
        self.assertTrue(df.index.equals(df_2.index))

    def test_read_mulit_symbol(self):
        """测试读取多支股票，一个Column"""
        codes = ('601398', '601939', '601988')
        df = DailyReader(codes).read()
        self.assertFalse(df.empty)
        for c in codes:
            self.assertTrue((c + '_Close') in df.columns)
        print(df.tail())

    def test_read_mulit_symbol_mulit_column(self):
        """测试读取多支股票，多个Column。是否正常增加前缀"""
        columns = ['Close', 'Open']
        codes = ('601398', '601939')
        df = DailyReader(codes, columns=columns).read()
        self.assertFalse(df.empty)
        for c in codes:
            for col in columns:
                self.assertTrue((c + '_' + col) in df.columns)
        print(df.tail())

    def test_read_sort(self):
        """测试排序是否有效"""
        code = '601398'
        df = DailyReader(code).read()
        df_desc = DailyReader(code, sort_index='desc').read()
        self.assertTrue(df.iloc[-1].equals(df_desc.iloc[0]))

    def test_read_leave_zs(self):
        """测试保留指数列"""
        code = '601398'
        df = DailyReader(code, drop_zs_columns=False).read()
        self.assertFalse(df.empty)
        self.assertTrue('sh000001_Close' in df.columns)
        print(df.tail())

    def test_read_valueerror(self):
        code = '601398'
        self.assertRaises(ValueError, DailyReader, None)
        self.assertRaises(ValueError, DailyReader, code, reader=None)
        self.assertRaises(ValueError, DailyReader, code, columns=None)
        self.assertRaises(ValueError, DailyReader, code, zs_symbol=None)
        self.assertRaises(RuntimeError, DailyReader(code,
                                                    zs_symbol='zs000001').read)

    def test_demo(self):
        df = DailyReader((601398, 601939), drop_zs_columns=False).read()
        print(df.tail())


if __name__ == '__main__':
    unittest.main()
