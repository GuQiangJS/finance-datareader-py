# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import re
import time

import pandas as pd
from pandas_datareader.base import _BaseReader

__all__ = ['get_sse_symbols']
_RE = re.compile('val:"(6\d{5})",val2:"(.*)",val3:"(.*)"')
_ticker_cache = None


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
            r'http://www.sse.com.cn/js/common/ssesuggestdataAll.js')
        matches = _RE.finditer(response.text)
        for match in matches:
            result.append({'symbol': match.group(1), 'name': match.group(2)})
        data = pd.DataFrame(result)
        data.set_index("symbol", inplace=True)
        return data
    finally:
        reader.close()
