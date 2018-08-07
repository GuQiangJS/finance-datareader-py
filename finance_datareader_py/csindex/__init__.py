# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import pandas as pd
from pandas import read_excel


def get_stock_holdings(index: str):
    """ 从 中证指数有限公司 获取指数的成分列表

    Args:
        index: 指数代码

    Returns:
        ``pandas.DataFrame``:

    Examples:
        .. code-block:: python

            from finance_datareader_py.csindex import get_stock_holdings

            df = get_stock_holdings('000300')

            print(df)

        .. code-block::

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


def get_stock_holdings_weight(index: str):
    """ 从 中证指数有限公司 获取指数的成分权重

        Args:
            index: 指数代码

        Returns:
            ``pandas.DataFrame``:

        Examples:
            .. code-block:: python

                from finance_datareader_py.csindex import get_stock_holdings_weight

                df = get_stock_holdings('000300')

                print(df)

            .. code-block::

                symbol  name      权重(%)Weight(%)
                600000  浦发银行            1.11
                600008  首创股份            0.10
                600009  上海机场            0.54
                600010  包钢股份            0.21
                ...      ...
        """
    if not index:
        raise ValueError()

    url = 'http://www.csindex.com.cn/uploads/file/autofile/' \
          'closeweight/{0}closeweight.xls'.format(index)

    df = read_excel(url, convert_float=False, dtype=object, usecols=[4, 5, 8])
    df.rename(columns={'成分券代码Constituent Code': 'symbol',
                       '成分券名称Constituent Name': 'name'}, inplace=True)
    df.set_index("symbol", inplace=True)
    df['权重(%)Weight(%)'] = pd.to_numeric(df['权重(%)Weight(%)'],
                                         downcast='float')
    return df
