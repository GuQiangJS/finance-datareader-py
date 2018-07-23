# Copyright (C) 2018 GuQiangJs. https://github.com/GuQiangJS
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.csrc import category


class csrc_TestCase(unittest.TestCase):
    def test_get_get_pdf(self):
        nums = (0, 1, 15, 30)
        # 当前一页20条，最多只有22条。截止2018一季度
        for i in nums:
            d = category.get_pdf(top=i)
            if i == 0:
                self.assertFalse(d)
                continue
            elif i >= 22:
                self.assertTrue(d)
                self.assertTrue(0 < len(d) < i)
            else:
                self.assertEqual(len(d), i)
            print('-------------------------')
            print(d)


if __name__ == '__main__':
    unittest.main()
