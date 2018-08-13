Python 金融数据读取器
=====================

.. image:: https://api.travis-ci.org/GuQiangJS/finance-datareader-py.svg?branch=master
    :target: https://travis-ci.org/GuQiangJS/finance-datareader-py
    
.. image:: https://coveralls.io/repos/github/GuQiangJS/finance-datareader-py/badge.svg?branch=master
    :target: https://coveralls.io/github/GuQiangJS/finance-datareader-py?branch=master



基于 ``pandas-datareader`` 开发，用来读取 上证、深证（股票列表、每日成交汇总）

依赖
~~~~

使用 finance-datareader-py 依赖于以下包：

* xlrd
* pandas-datareader
* numpy
* beautifulsoup4

编译帮助文档时使用：

* sphinx
* sphinxcontrib-napoleon

快速安装
--------

安装发布版本
~~~~~~~~~~~~

.. code-block:: shell

   $ pip install finance-datareader-py

安装开发版本
~~~~~~~~~~~~

.. code-block:: shell

   $ pip install git+https://github.com/GuQiangJS/finance-datareader-py.git

文档
----

`开发文档 <https://guqiangjs.github.io/finance-datareader-py/devel/>`__

使用示例
--------

.. code-block:: python

    >>> from finance_datareader_py.sohu.daily import SohuDailyReader

    >>> df = SohuDailyReader(symbols='000002').read()

    >>> print(df.tail())

                Open  Close  Change  Quote   Low  High    Volume  Turnover  Rate
    Date
    2004-10-14  5.80   5.67   -0.12  -2.07  5.56  5.80  265167.0  15041.02  1.68
    2004-10-13  5.81   5.79    0.00   0.00  5.69  5.85  252039.0  14604.28  1.60
    2004-10-12  5.53   5.79    0.25   4.51  5.50  5.87  600869.0  34637.16  3.82
    2004-10-11  5.56   5.54   -0.02  -0.36  5.51  5.65  264020.0  14775.34  1.68
    2004-10-08  5.42   5.56    0.14   2.58  5.28  5.60  117074.0   6368.60  0.74
