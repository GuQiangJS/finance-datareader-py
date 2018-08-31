Python 金融数据读取器
==========================================

.. image:: https://badge.fury.io/py/finance-datareader-py.svg
    :target: https://badge.fury.io/py/finance-datareader-py

.. image:: https://api.travis-ci.org/GuQiangJS/finance-datareader-py.svg?branch=master
    :target: https://travis-ci.org/GuQiangJS/finance-datareader-py
    
.. image:: https://coveralls.io/repos/github/GuQiangJS/finance-datareader-py/badge.svg?branch=master
    :target: https://coveralls.io/github/GuQiangJS/finance-datareader-py?branch=master



基于 ``pandas-datareader`` 开发，用来读取 上证、深证（股票列表、每日成交汇总）

依赖
~~~~~~~~~~

使用 finance-datareader-py 依赖于以下包：

* xlrd
* pandas-datareader
* numpy
* beautifulsoup4

编译帮助文档时使用：

* sphinx
* sphinxcontrib-napoleon

快速安装
~~~~~~~~~~~~~~~~

安装发布版本
------------------------

.. code-block:: shell

   $ pip install finance-datareader-py

安装开发版本
------------------------

.. code-block:: shell

   $ pip install git+https://github.com/GuQiangJS/finance-datareader-py.git

文档
~~~~~~~~

`开发文档 <https://guqiangjs.github.io/finance-datareader-py/devel/>`__

使用示例
~~~~~~~~~~~~~~~~

* 一次获取多支股票的收盘价。并自动填充停牌数据。

    .. code-block:: python

        >>> from finance_datareader_py import DailyReader
        >>> df = DailyReader((601398,601939), drop_zs_columns=False).read()
        >>> print(df.tail())

                    sh000001_Close  601398_Close  601939_Close
        Date
        2018-08-17         2668.97          5.26          6.52
        2018-08-20         2698.47          5.36          6.66
        2018-08-21         2733.83          5.40          6.72
        2018-08-22         2714.61          5.39          6.70
        2018-08-23         2724.62          5.40          6.69

* 获取上证股票列表

    .. code-block:: python

        >>> from finance_datareader_py.sse import get_sse_symbols
        >>> print(get_sse_symbols().tail())

                  name  symbol
        1425  洛阳钼业  603993
        1426  中新科技  603996
        1427  继峰股份  603997
        1428  方盛制药  603998
        1429  读者传媒  603999

* 读取上市公司主要财务指标

    .. code-block:: python

        >>> from finance_datareader_py.sohu import FinancialIndicatorReader
        >>> df = FinancialIndicatorReader('601398').read()
        >>> print(df.iloc[0][:-1])

        净资产收益率加权(%)                 3.85
        股东权益不含少数股东权益(万元)       217151000
        流动负债(万元)                      --
        总负债(万元)               2430887600
        流动资产(万元)                      --
        总资产(万元)               2649378100
        现金及现金等价物净增加额(万元)        -5756000
        经营活动产生的现金流量净额(万元)        6216000
        净利润(扣除非经常性损益后)(万元)       7779500
        净利润(万元)                  7880200
        利润总额(万元)                10164600
        营业外收支净额(万元)               136000
        投资收益(万元)                  267800
        营业利润(万元)                10028600
        主营业务利润(万元)              10028600
        主营业务收入(万元)              19719800
        每股经营活动产生的现金流量净额(元)            --
        每股净资产(元)                    5.85
        Name: 2018-03-31 00:00:00, dtype: object
