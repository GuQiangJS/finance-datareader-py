finance-datareader-py
=======================
    
.. image:: https://api.travis-ci.org/GuQiangJS/finance-datareader-py.svg?branch=master
    :target: https://travis-ci.org/GuQiangJS/finance-datareader-py
   
.. image:: https://coveralls.io/repos/github/GuQiangJS/finance-datareader-py/badge.svg?branch=master
   :target: https://coveralls.io/github/GuQiangJS/finance-datareader-py?branch=master


Python 金融数据读取器

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
~~~~~~~~~

.. code-block:: shell

    $ pip install git+https://github.com/GuQiangJS/finance-datareader-py.git

文档
~~~~~

`开发文档 <https://guqiangjs.github.io/finance-datareader-py/devel/>`__
会在每次提交变更后自动生成。

使用示例
~~~~~~~~~

.. code-block:: python

    In[2]: from finance_datareader_py.netease.daily import NetEaseDailyReader
    In[3]: df = NetEaseDailyReader(symbols='000002').read()
    In[4]: df.tail()
    
.. code-block::

    Out[5]:
                Close  High   Low  Open Change    Quote    Rate    Volume  Turnover
    2018-07-04  23.00  23.75  23.00  23.46  -0.42  -1.7933  0.2570  249881.0  58247.0  
    2018-07-05  23.05  23.41  22.85  23.02   0.05   0.2174  0.2749  267279.0  61939.0  
    2018-07-06  23.21  23.60  22.65  23.34   0.16   0.6941  0.3568  346930.0  80511.0 
    2018-07-09  24.01  24.05  23.37  23.37    0.8   3.4468  0.4161  404627.0  96480.0 
    2018-07-10  24.15  24.49  23.77  24.20   0.14   0.5831  0.4003  389259.0  93653.0
