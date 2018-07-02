finance-datareader-py
=======================

Python 金融数据读取器

基于 ``pandas-datareader`` 开发，用来读取 上证、深证（股票列表、每日成交汇总）

依赖
~~~~

使用 finance-datareader-py 依赖于以下包：

* pandas-datareader
* numpy
* beautifulsoup4

编译帮助文档时使用：

* sphinx

快速安装
~~~~~~~~~

.. code-block:: shell

    $ pip install git+https://github.com/GuQiangJS/finance-datareader-py.git

使用示例
~~~~~~~~~

.. code-block:: python

    In[2]: from finance_datareader_py.netease.daily import NetEaseDailyReader
    In[3]: df = NetEaseDailyReader(symbols='000002').read()
    In[4]: df[1:5]
    
    Out[5]:
                Close  High   Low  Open Change    Quote    Rate    Volume  Turnover
    2004-10-11   5.54  5.65  5.51  5.56  -0.02  -0.3597  1.6744  264020.0   14775.0
    2004-10-12   5.79  5.87  5.50  5.53   0.25   4.5126  3.8106  600869.0   34637.0
    2004-10-13   5.79  5.85  5.69  5.81    0.0      0.0  1.5984  252039.0   14604.0
    2004-10-14   5.67  5.80  5.56  5.80  -0.12  -2.0725  1.6816  265167.0   15041.0
