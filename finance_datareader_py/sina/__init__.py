# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import re
import time

import pandas as pd
from bs4 import BeautifulSoup as bs
from pandas_datareader.base import _BaseReader

_dividends_cache = None


def get_dividends(symbol: str, retry_count=3, timeout=30, pause=None):
    """从新浪获取分红配送数据

    Args:
        symbol: 股票代码
        retry_count:
        timeout:
        pause:

    Returns:
        ``[DataFrame,DataFrame]``

        **任意数据表无数据时返回None**

    Examples:
        .. testcode:: python

            from finance_datareader_py.sina import get_dividends

            df1, df2 = get_dividends('000541')

            print(df1)
            print('------------')
            print(df2)

        .. testoutput::

            公告日期     派息(税前)(元)      红股上市日      股权登记日  转增(股)  送股(股)      除权除息日
            2018-05-05      3.290        NaT 2018-05-10    1.0    0.0 2018-05-11
            2017-06-01      4.200        NaT 2017-06-07    0.0    0.0 2017-06-08
            2016-05-07      0.125        NaT 2016-05-12    0.0    0.0 2016-05-13
            2015-06-05      2.200        NaT 2015-06-11    3.0    0.0 2015-06-12
            ------------
            公告日期     募集资金合计(元)     基准股本(万股)      缴款终止日      缴款起始日      股权登记日  \

            1994-12-24        NaN  115755000.0 1995-01-27 1995-01-16 1995-01-03

            公告日期         配股上市日  配股价格(元)  配股方案(每10股配股股数)        除权日
            1994-12-24 1995-02-22      8.0             2.0 1995-01-04

        """
    # http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/000541.phtml

    global _dividends_cache
    if timeout < 0:
        raise ValueError(
            'timeout must be >= 0, not {timeout}'.format(timeout=timeout))

    if pause is None:
        pause = timeout / 3
    elif pause < 0:
        raise ValueError('pause must be >= 0, not {pause}'.format(pause=pause))

    if _dividends_cache is None or symbol not in _dividends_cache:
        if _dividends_cache is None:
            _dividends_cache = {}
        while retry_count > 0:
            try:
                _dividends_cache[symbol] = _download_dividends(symbol)
                retry_count = -1
            except Exception:
                # retry on any exception
                if retry_count <= 0:
                    raise
                else:
                    retry_count -= 1
                    time.sleep(pause)

    return _dividends_cache[symbol] if symbol in _dividends_cache else [None,
                                                                        None]


def _download_dividends(symbol: str):
    reader = _BaseReader('')

    try:
        response = reader._get_response(
            r'http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/{0}.phtml'.format(
                symbol))
        txt = str(response.content, encoding='gb2312')
        fh = re.search(
            '<!--分红 begin-->[\s\S]*<tbody>([\s\S]*)<\/tbody>[\s\S]*<!--分红 end-->',
            txt)
        pg = re.search(
            '<!--配股 begin-->[\s\S]*<tbody>([\s\S]*)<\/tbody>[\s\S]*<!--配股 end-->',
            txt)
        df1, df2 = None, None
        # 分红数据
        r = _parse_body(bs(fh.group(1), 'lxml'), _parse_divided_line)
        if r:
            df1 = _translate_dtype(pd.DataFrame(r)).set_index('公告日期')
        # 配股数据
        r = _parse_body(bs(pg.group(1), 'lxml'), _parse_allotment_line)
        if r:
            df2 = _translate_dtype(pd.DataFrame(r)).set_index('公告日期')
    except Exception:
        raise
    finally:
        reader.close()
    return [df1, df2]


def _translate_dtype(df):
    """转换每一列的格式

    包含 `日` 字的被认为是日期，转换为 `datetime`。其他转换为 `float`。无法转换的被转换为 `NaN`。

    :param df:
    :return:
    """
    if df is not None and not df.empty:
        for col in df.columns:
            if '日' in col:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d',
                                         errors='coerce')
            else:
                df[col] = pd.to_numeric(df[col], downcast='float',
                                        errors='coerce')
    return df


def _parse_body(tbody, func_parse_line):
    """解析 tbody 内容

    :param tbody:
    :param func_parse_line: 解析每一行用的方法
    :return:
    """
    if not tbody:
        return None
    result = []
    for tr in tbody.find_all('tr'):
        d = func_parse_line(tr)
        if d:
            result.append(d)
    return result


def _parse_divided_line(tr):
    """解析分红数据tr行

    :return:
    """
    if not tr:
        return None
    tds = tr.find_all('td')
    if tds:
        return {
            '公告日期': tds[0].text.strip(),
            '送股(股)': tds[1].text.strip(),
            '转增(股)': tds[2].text.strip(),
            '派息(税前)(元)': tds[3].text.strip(),
            '除权除息日': tds[5].text.strip(),
            '股权登记日': tds[6].text.strip(),
            '红股上市日': tds[7].text.strip()
        }
    return None


def _parse_allotment_line(tr):
    """解析配股数据tr行

    :param tr:
    :return:
    """
    if not tr:
        return None
    tds = tr.find_all('td')
    if tds:
        return {
            '公告日期': tds[0].text.strip(),
            '配股方案(每10股配股股数)': tds[1].text.strip(),
            '配股价格(元)': tds[2].text.strip(),
            '基准股本(万股)': tds[3].text.strip(),
            '除权日': tds[4].text.strip(),
            '股权登记日': tds[5].text.strip(),
            '缴款起始日': tds[6].text.strip(),
            '缴款终止日': tds[7].text.strip(),
            '配股上市日': tds[8].text.strip(),
            '募集资金合计(元)': tds[9].text.strip()
        }
    return None
