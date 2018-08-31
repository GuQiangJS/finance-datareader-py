# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import datetime
import json
import re
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from pandas_datareader.base import _BaseReader

import finance_datareader_py
from finance_datareader_py import _AbsDailyReader

_dividends_cache = None


def _parse_symbol(symbol):
    """深市前加 sz，沪市前加 sh

    Args:
        symbol (str): 股票代码
    """
    return ('sh' if symbol[0] == '6' else 'sz') + symbol


class SinaQuoteReader(_AbsDailyReader):
    """从 新浪 获取指定股票（或集合）的最新价格信息

    Args:
        symbols (str, List[str]): 股票代码（或集合）
        start (datetime.date): 开始日期。默认值：None。**此方法不用该参数**。
        end (datetime.date): 结束日期。默认值：None。**此方法不用该参数**。
        retry_count: 重试次数
        pause: 重试间隔时间
        session:
        chunksize:

    Returns:
        当 `symbols` 是字符串的情况下，返回 ``pandas.DataFrame``，
        否则返回 ``pandas.Panel``

    Examples:
        .. code-block:: python

            >>> from finance_datareader_py.sina import SinaQuoteReader
            >>> print(SinaQuoteReader('000002').read())
                         datetime  price
            0 2018-08-21 15:05:03  23.91

            >>> from finance_datareader_py.sina import SinaQuoteReader
            >>> l = ('000002', '300027', '000927')
            >>> p = SinaQuoteReader(l).read()
            >>> for s in l:
            >>>     print('{:8}{:>7} {}.'.format(s, p['price'][s][0], p['datetime'][s][0]))

            000002    23.91 2018-08-21 15:05:03.
            300027     5.72 2018-08-21 15:05:03.
            000927      3.4 2018-08-21 15:05:03.

    """

    def __init__(self, symbols=None, start=None, end=None,
                 retry_count=3, pause=1, session=None,
                 chunksize=25):
        super(SinaQuoteReader, self).__init__(symbols, start, end,
                                              retry_count, pause, session,
                                              chunksize)
        self._encoding = 'gb2312'

    @property
    def url(self):
        # https://hq.sinajs.cn/?list=sz000002,sz000003
        return "https://hq.sinajs.cn/"

    def _get_params(self, *args, **kwargs):
        return 'list={0}'.format(_parse_symbol(args[0]))
        # if isinstance(self.symbols, compat.string_types):
        #     return 'list={0}'.format(_parse_symbol(self.symbols))
        # else:
        #     return 'list=' + ','.join([_parse_symbol(symbol) for symbol in
        #                                self.symbols])

    def _read_lines(self, out):
        # var hq_str_sz000002="万 科Ａ,23.390,23.350,23.870,23.910,23.220,23.870,23.880,38877394,917414197.170,3600,23.870,32400,23.860,33700,23.850,6400,23.840,4800,23.830,10900,23.880,26500,23.890,78800,23.900,45800,23.910,59800,23.920,2018-08-21,13:54:42,00";
        line = out.readline()
        s = line.split(',')
        dt = datetime.datetime.strptime(s[-3] + s[-2], '%Y-%m-%d%H:%M:%S')
        return pd.DataFrame({'price': [float(s[3])], 'datetime': [dt]})


def get_cpi() -> pd.DataFrame:
    """ 从 Sina 获取 CPI 居民消费价格指数。

    Returns: 返回获取到的数据表。数据从1990.1开始。

    Examples:

        .. code-block:: python

            >>> from finance_datareader_py.sina import get_cpi
            >>> print(get_cpi().tail())

                     价格指数
            统计月份
            1990.5  102.7
            1990.4  103.2
            1990.3  103.4
            1990.2  104.4
            1990.1  104.3

    """

    c = finance_datareader_py._random()
    start = 0
    num = (datetime.date.today().year + 1 - 1990) * 12

    url = 'http://money.finance.sina.com.cn/mac/api/jsonp.php' \
          '/SINAREMOTECALLCALLBACK{' \
          'c}/MacPage_Service.get_pagedata?cate=price&event=0&from={' \
          'start}&num={num}&condition=&_={c}'.format(c=c, start=start, num=num)
    return _get_mac_price(url, columns=['统计月份', '价格指数'])[0] \
        .set_index('统计月份') \
        .astype(np.float64)


def _get_mac_price(url, columns=None, index=None, dtype=None):
    """从新浪 中国宏观经济数据页 分析数据
    # http://finance.sina.com.cn/mac/#price-0-0-31-2

    Args:
        url:
        columns:
        index:

    Returns: 返回 [数据表,url源码]

    """
    reader = _BaseReader(url)
    try:
        rep = reader._get_response(url)
        if rep:
            txt = rep.text
            m = re.compile('count:"\d+",data:(.*)}').search(txt)
            if m:
                df = pd.DataFrame(json.loads(m.group(1)),
                                  columns=columns, index=index, dtype=dtype)
                return df, txt
    except Exception:
        raise
    finally:
        reader.close()
    return None, None


def get_measure_of_money_supply():
    """ 从 Sina 获取 中国货币供应量数据。

    Returns: 返回获取到的数据表。数据从1978.1开始。

    Examples:

        .. code-block:: python

            >>> df = get_measure_of_money_supply()
            >>> print(df.iloc[0][df.columns[0]])
            >>> print(df.index[-1])
            >>> print(df.columns)

            1776196.11
            1978.8
            Index(['货币和准货币（广义货币M2）(亿元)', '货币和准货币（广义货币M2）同比增长(%)', '货币(狭义货币M1)(亿元)',
                   '货币(狭义货币M1)同比增长(%)', '流通中现金(M0)(亿元)', '流通中现金(M0)同比增长(%)', '活期存款(亿元)',
                   '活期存款同比增长(%)', '准货币(亿元)', '准货币同比增长(%)', '定期存款(亿元)', '定期存款同比增长(%)',
                   '储蓄存款(亿元)', '储蓄存款同比增长(%)', '其他存款(亿元)', '其他存款同比增长(%)'],
                  dtype='object')

    """
    c = finance_datareader_py._random()
    start = 0
    num = (datetime.date.today().year + 1 - 1978) * 12

    url = 'http://money.finance.sina.com.cn/mac/api/jsonp.php' \
          '/SINAREMOTECALLCALLBACK{c}/MacPage_Service.get_pagedata' \
          '?cate=fininfo&event=1&from={start}&num={num}&condition=&_={' \
          'c}'.format(c=c, start=start, num=num)
    df, txt = _get_mac_price(url)
    title = re.compile('all:(.*),defaultItems:').search(txt).group(1)
    columns = {}
    index = 0
    for t in json.loads(title):
        columns[index] = t[1] + ('({0})'.format(t[2]) if len(t) > 2 else '')
        index = index + 1
    df = df.rename(columns=columns)
    df = df.set_index('统计时间')
    df = df.astype(np.float64)
    return df


def get_dividends(symbol: str, retry_count=3, timeout=30, pause=None):
    """从新浪获取分红配送数据

    Args:
        symbol: 股票代码
        retry_count:
        timeout:
        pause:

    Returns:
        ``[DataFrame,DataFrame]``:

        任意数据表无数据时返回 空白的 ``pandas.DataFrame`` 。
        参见 ``pandas.DataFrame.empty``。

    Examples:
        .. code-block:: python

            >>> from finance_datareader_py.sina import get_dividends

            >>> df1, df2 = get_dividends('000541')

            >>> print(df1.tail())

                        派息(税前)(元)      红股上市日      股权登记日  转增(股)  送股(股)      除权除息日
            公告日期
            1997-07-22       4.77        NaT 1997-07-29    0.0    0.0 1997-07-30
            1996-09-12       0.00 1996-09-19 1996-09-16    5.0    0.0 1996-09-17
            1996-05-30       6.80        NaT 1996-06-07    0.0    0.0 1996-06-10
            1995-07-21       8.10        NaT 1995-07-25    0.0    0.0 1995-07-26
            1994-04-23       3.00        NaT 1994-05-05    1.0    4.0 1994-05-06

            >>> print(df2.tail())

                        募集资金合计(元)     基准股本(万股)      缴款终止日      缴款起始日      股权登记日  \
            公告日期
            1994-12-24        NaN  115755000.0 1995-01-27 1995-01-16 1995-01-03

                            配股上市日  配股价格(元)  配股方案(每10股配股股数)        除权日
            公告日期
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

    return _dividends_cache[symbol] if symbol in _dividends_cache else [
        pd.DataFrame(), pd.DataFrame()]


def _download_dividends(symbol: str):
    reader = _BaseReader('')

    try:
        response = reader._get_response(r'http://vip.stock.finance.sina.com.cn/'
                                        r'corp/go.php/vISSUE_ShareBonus/stockid'
                                        r'/{0}.phtml'.format(symbol),
                                        _AbsDailyReader._default_headers())
        txt = str(response.content, encoding='gb2312')
        fh = re.search(
            '<!--分红 begin-->[\s\S]*<tbody>([\s\S]*)<\/tbody>[\s\S]*<!--分红 end-->',
            txt)
        pg = re.search(
            '<!--配股 begin-->[\s\S]*<tbody>([\s\S]*)<\/tbody>[\s\S]*<!--配股 end-->',
            txt)
        df1, df2 = pd.DataFrame(), pd.DataFrame()
        # 分红数据
        r = _parse_body(bs(fh.group(1), 'lxml'), _parse_divided_line)
        if r:
            df1 = _create_df(r)
        # 配股数据
        r = _parse_body(bs(pg.group(1), 'lxml'), _parse_allotment_line)
        if r:
            df2 = _create_df(r)
    except Exception:
        raise
    finally:
        reader.close()
    return [df1, df2]


def _create_df(r):
    df = _translate_dtype(pd.DataFrame(r))
    df = df.replace({'--': np.nan, '': np.nan})
    return df


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
                df[col] = df[col].astype(np.float64, errors='ignore', copy=True)
    return df


def _parse_body(tbody, func_parse_line):
    """解析 tbody 内容"""
    if not tbody:
        return None
    result = []
    for tr in tbody.find_all('tr'):
        d = func_parse_line(tr)
        if d:
            result.append(d)
    return result


def _parse_divided_line(tr):
    """解析分红数据tr行"""
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


def _get_value(v):
    result = v.text.strip()
    return result if result else np.nan


def _parse_allotment_line(tr):
    """解析配股数据tr行"""
    if not tr:
        return None
    tds = tr.find_all('td')
    if tds and len(tds) >= 9:
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
