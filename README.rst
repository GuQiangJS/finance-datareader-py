Python 金融数据读取器
=====================

.. image:: https://api.travis-ci.org/GuQiangJS/finance-datareader-py.svg?branch=master
    :target: https://travis-ci.org/GuQiangJS/finance-datareader-py
    
.. image:: https://coveralls.io/repos/github/GuQiangJS/finance-datareader-py/badge.svg?branch=master
    :target: https://coveralls.io/github/GuQiangJS/finance-datareader-py?branch=master



基于 ``pandas-datareader`` 开发，用来读取 上证、深证（股票列表、每日成交汇总）

依赖
~~~~~

使用 finance-datareader-py 依赖于以下包：

* xlrd
* pandas-datareader
* numpy
* beautifulsoup4

编译帮助文档时使用：

* sphinx
* sphinxcontrib-napoleon

快速安装
~~~~~~~~

安装发布版本
------------

.. code-block:: shell

   $ pip install finance-datareader-py

安装开发版本
------------

.. code-block:: shell

   $ pip install git+https://github.com/GuQiangJS/finance-datareader-py.git

文档
~~~~

`开发文档 <https://guqiangjs.github.io/finance-datareader-py/devel/>`__

使用示例
~~~~~~~~

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
