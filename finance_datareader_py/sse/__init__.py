# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import re
import time

import pandas as pd
from pandas_datareader.base import _BaseReader

from finance_datareader_py import _AbsDailyReader

__all__ = ['get_sse_symbols', 'get_dividends']
# 获取A股名称数据时的正则
_RE_SYMBOLS = re.compile('val:"(6\d{5})",val2:"(.*)",val3:"(.*)"')
# 获取分红数据时的正则
_RE_DIVIDENDS = re.compile('"result":(.*),"sqlId"')
_ticker_cache = None
_dividends_cache = None


def get_sse_symbols(retry_count=3, timeout=30, pause=None):
    """获取最新的上海证券交易所交易的 A股 名称数据

    Args:
        retry_count: 重试次数
        timeout: 超时时间
        pause:

    Returns:
        ``pandas.DataFrame``:

    Examples:
        .. testcode:: python

            from finance_datareader_py.sse import get_sse_symbols

            df2 = get_sse_symbols()

            print(df2)

        .. testoutput::

            symbol   name
            600000  浦发银行
            600004  白云机场
            600006  东风汽车
            600007  中国国贸
    """
    global _ticker_cache
    if timeout < 0:
        raise ValueError(
            'timeout must be >= 0, not {timeout}'.format(timeout=timeout))

    if pause is None:
        pause = timeout / 3
    elif pause < 0:
        raise ValueError('pause must be >= 0, not {pause}'.format(pause=pause))

    if _ticker_cache is None:
        while retry_count > 0:
            try:
                _ticker_cache = _download_sse_symbols(timeout=timeout)
                retry_count = -1
            except Exception:
                # retry on any exception
                if retry_count <= 0:
                    raise
                else:
                    retry_count -= 1
                    time.sleep(pause)

    return _ticker_cache


def _download_sse_symbols(timeout):
    reader = _BaseReader('')

    try:
        result = []
        response = reader._get_response(
            r'http://www.sse.com.cn/js/common/ssesuggestdataAll.js',
            headers=_AbsDailyReader._headers)
        matches = _RE_SYMBOLS.finditer(response.text)
        for match in matches:
            result.append({'symbol': match.group(1), 'name': match.group(2)})
        data = pd.DataFrame(result)
        data.set_index("symbol", inplace=True)
        return data
    finally:
        reader.close()


def get_dividends(symbol: str, retry_count=3, timeout=30, pause=None):
    """从 上海证券交易所 获取分红配送数据

    **只能获取上证数据**

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
        .. testcode:: python

            from finance_datareader_py.sse import get_dividends

            df1, df2 = get_dividends('600006')

            print(df1)
            print('------------')
            print(df2)

        .. testoutput::

                        每股红利(除税)  每股红利(含税)       除息交易日  股权登记日总股本(万股)  除息前日收盘价   除息报价
            股权登记日
            2018-06-15   0.03030    0.0303  2018-06-19        200000     4.34   4.35
            2017-07-13   0.03300    0.0330  2017-07-14        200000     5.87   5.89
            2016-06-29   0.05200    0.0520  2016-06-30        200000     8.95   9.00
            2015-07-23   0.02014    0.0212  2015-07-24        200000    10.33  10.18
            2014-06-19   0.00722    0.0076  2014-06-20        200000     2.91   2.92
            2013-06-14   0.00314    0.0033  2013-06-17        200000     3.07   3.07
            ------------
                        公告刊登日  送股比例(10:?)       除权基准日  股权登记日总股本(万股)       红股上市日
            股权登记日
            2004-06-10  2004-06-07          10  2004-06-11        100000  2004-06-14

        """

    if not symbol:
        raise ValueError('symbol')
    if not symbol.startswith('6'):
        raise ValueError('只能获取上证数据')

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
    try:
        reader = _AbsDailyReader('')
        reader._append_header('Host', 'query.sse.com.cn')
        reader._append_header('Referer',
                              'http://www.sse.com.cn/assortment/stock/list'
                              '/info/profit/index.shtml?COMPANY_CODE={0}'
                              .format(symbol))

        df1 = _download_fh(reader, symbol)
        df2 = _download_sg(reader, symbol)
    except Exception:
        raise
    finally:
        reader.close()
        df1 = df1 if df1 is not None else pd.DataFrame()
        df2 = df2 if df2 is not None else pd.DataFrame()
    return [df1, df2]


def _download_sg(reader, symbol: str):
    """获取送股数据"""
    url = 'http://query.sse.com.cn/commonQuery.do?sqlId' \
          '=COMMON_SSE_ZQPZ_GG_LYFP_AGSG_L&productid={0}'.format(symbol)

    try:
        rep = reader._get_response(url)
        if rep:
            m = _RE_DIVIDENDS.search(rep.text)
            if m:
                return _parse_sg_dataframe(pd.read_json(m.group(1)))
    except Exception:
        raise
    return None


def _download_fh(reader, symbol: str):
    """获取分红数据"""

    url = 'http://query.sse.com.cn/commonQuery.do?sqlId' \
          '=COMMON_SSE_ZQPZ_GG_LYFP_AGFH_L&productid={0}'.format(symbol)

    try:
        rep = reader._get_response(url)
        if rep:
            m = _RE_DIVIDENDS.search(rep.text)
            if m:
                return _parse_fh_dataframe(pd.read_json(m.group(1)))
    except Exception:
        raise
    return None


def _parse_fhsg_dataframe(df, rename_columns: dict, drop_other=True,
                          index_column=None):
    """处理分红送股表格，重命名表头

    Args:
        df:
        rename_columns: 重命名表头使用的 dict
        drop_other: 是否删除不在 rename_columns 中的列
        index_column: 设为索引的列

    Returns:

    """
    if df is None or df.empty:
        return pd.DataFrame()
    if drop_other:
        remove_columns = list(
            set(df.columns).difference(set(rename_columns.keys())))
        df.drop(columns=remove_columns, inplace=True)
    df.rename(columns=rename_columns, inplace=True)
    if index_column and index_column in df.columns:
        df.set_index(index_column, inplace=True)
    return df


def _parse_fh_dataframe(df):
    """处理分红表格，删除不需要的列，给列头赋值"""
    """
    {
        每股红利(除税) "DIVIDEND_PER_SHARE1_A": "0.08",
        每股红利(含税) "DIVIDEND_PER_SHARE2_A": "0.1",
        ** "SECURITY_NAME_A": "东风汽车",
        ** "TOTAL_DIVIDEND_A": "-",
        ** "SECURITY_CODE_A": "600006",
        ** "COMPANY_CODE": "600006",
        ** "A_SHARES": "-",
        除息交易日 "EX_DIVIDEND_DATE_A": "2000-06-26",
        除息报价 "OPEN_PRICE_A": "5.98",
        ** "FULL_NAME": "东风汽车股份有限公司",
        除息前日收盘价 "LAST_CLOSE_PRICE_A": "5.93",
        股权登记日总股本(万股) "ISS_VOL": "100000",
        股权登记日 "RECORD_DATE_A": "2000-06-23"
    }
    """
    return _parse_fhsg_dataframe(df, {'DIVIDEND_PER_SHARE1_A': '每股红利(除税)',
                                      'DIVIDEND_PER_SHARE2_A': '每股红利(含税)',
                                      'EX_DIVIDEND_DATE_A': '除息交易日',
                                      'OPEN_PRICE_A': '除息报价',
                                      'LAST_CLOSE_PRICE_A': '除息前日收盘价',
                                      'ISS_VOL': '股权登记日总股本(万股)',
                                      'RECORD_DATE_A': '股权登记日'},
                                 index_column='股权登记日')


def _parse_sg_dataframe(df):
    """处理送股表格，删除不需要的列，给列头赋值"""
    """
    {
        送股比例(10:?) "BONUS_RATE": "10", 
        公告刊登日 "ANNOUNCE_DATE": "2004-06-07", 
        *** "ANNOUNCE_DESTINATION": "-", 
        红股上市日 "TRADE_DATE_A": "2004-06-14", 
        *** "SECURITY_NAME_A": "东风汽车", 
        股权登记日总股本(万股) "ISS_VOL": "100000", 
        *** "COMPANY_NAME": "东风汽车股份有限公司", 
        股权登记日 "RECORD_DATE_A": "2004-06-10", 
        "SECURITY_CODE_A": "600006", 
        除权基准日 "EX_RIGHT_DATE_A": "2004-06-11", 
        "COMPANY_CODE": "600006", 
        "CHANGE_RATE": "7"
        }
    """
    return _parse_fhsg_dataframe(df, {'BONUS_RATE': '送股比例(10:?)',
                                      'ANNOUNCE_DATE': '公告刊登日',
                                      'TRADE_DATE_A': '红股上市日',
                                      'ISS_VOL': '股权登记日总股本(万股)',
                                      'LAST_CLOSE_PRICE_A': '除息前日收盘价',
                                      'EX_RIGHT_DATE_A': '除权基准日',
                                      'RECORD_DATE_A': '股权登记日'},
                                 index_column='股权登记日')
