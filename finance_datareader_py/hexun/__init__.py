# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import numpy as np
from bs4 import BeautifulSoup as bs

from finance_datareader_py import _AbsDailyReader


def get_deposit_interest_rate():
    """从 和讯网 获取最新的人民币存款利率

    Returns:
        ``dict``:

    Examples:
        .. code-block:: python

            from finance_datareader_py.hexun import get_deposit_interest_rate

            print(get_deposit_interest_rate())

        .. code-block::

            {
                "日期": "2015-10-24",
                "上浮": 0,
                "活期": 0.35,
                "整存整取-3个月": 1.1,
                "整存整取-6个月": 1.3,
                "整存整取-一年": 1.5,
                "整存整取-二年": 2.1,
                "整存整取-三年": 2.75,
                "整存整取-五年": "--",
                "零存整取/整存零取-一年": 1.1,
                "零存整取/整存零取-三年": 1.3,
                "零存整取/整存零取-五年": "--",
                "协定存款": 1.15,
                "一天通知存款": 0.8,
                "七天通知存款": 1.35
            }

    """
    url = 'http://data.bank.hexun.com/ll/ckll.aspx'
    reader = _AbsDailyReader('')
    rep = reader._get_response(url)
    b = bs(rep.text, 'html.parser')
    reader.close()
    tbody_first_tr = b.find('tbody', attrs={'hasdata': 'true'}).contents[0]
    result = {}
    keys = ['日期', '上浮', '活期',
            '整存整取-3个月',
            '整存整取-6个月',
            '整存整取-一年',
            '整存整取-二年',
            '整存整取-三年',
            '整存整取-五年',
            '零存整取/整存零取-一年',
            '零存整取/整存零取-三年',
            '零存整取/整存零取-五年',
            '协定存款', '一天通知存款', '七天通知存款']
    tds = [td.text for td in tbody_first_tr.find_all('td')]
    for index in range(len(tds)):
        v = tds[index]
        if v.replace('.', '').isnumeric():
            v = np.float(v)
        # elif v == '--':
        #     v = np.nan
        result[keys[index]] = v
    return result
