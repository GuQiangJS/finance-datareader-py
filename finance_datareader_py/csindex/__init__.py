# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

from pandas import read_excel


def get_stock_holdings(index: str):
    """ 获取指数的成分列表

    Args:
        index: 指数代码

    Returns:
        .. testcode:: python

            from finance_datareader_py.csindex import get_stock_holdings

            df = get_stock_holdings('000300')

            print(df)

        .. testoutput::
            symbol  name
            600000  浦发银行
            600008  首创股份
            600009  上海机场
            600010  包钢股份
            ...      ...
    """
    if not index:
        raise ValueError()

    url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/{0}' \
          'cons.xls'.format(index)

    df = read_excel(url, convert_float=False, dtype=object, usecols=[4, 5])
    df.rename(columns={'成分券代码Constituent Code': 'symbol',
                       '成分券名称Constituent Name': 'name'}, inplace=True)
    df.set_index("symbol", inplace=True)
    return df
