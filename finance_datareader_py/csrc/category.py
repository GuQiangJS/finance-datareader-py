# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs
from pandas_datareader._utils import RemoteDataError
from pandas_datareader.base import _BaseReader

SRC = 'http://www.csrc.gov.cn/pub/newsite/scb/ssgshyfljg/'

__all__ = ['get_pdf']


def get_pdf(top=1):
    """ 从 中国证券监督管理委员会 获取 上市公司行业分类结果

    Args:
        top: 获取总条数。

    Returns: {文件名,pdf文件路径}

    Examples:
        .. testcode:: python

            from from finance_datareader_py.csrc import category

            df = category.get_pdf()

            print(df)

        .. testoutput::

            {
                "2018年1季度上市公司行业分类结果":
                "http://www.csrc.gov.cn/pub/newsite/scb/ssgshyfljg/201805/W020180521522232342268.pdf"
            }

    .. hint::
        对于 pdf 文件的解析，可以参考 `tabula-py <https://github.com/chezou/tabula-py>`_。

        .. testcode:: python

            import tabula

            df = tabula.read_pdf(r'http://www.csrc.gov.cn/pub/newsite/scb/ssgshyfljg/201805/W020180521522232342268.pdf',
                                 encoding='gbk', pages='all', format='json',
                                 silent=True, pandas_options={'header': 0})
            df = df.loc[df['上市公司代码'].str.isnumeric() == True]
            df = fillna(method='ffill')

            print(df)

        .. testoutput::

                   门类名称及代码 行业大类代码 行业大类名称  上市公司代码 上市公司简称
            0     农、林、牧、渔业     01     农业  000998   隆平高科
            1          (A)     01     农业  002041   登海种业
            2          (A)     01     农业  002772   众兴菌业
            3          (A)     01     农业  300087   荃银高科
            4          (A)     01     农业  300189   神农基因
            ...        ...    ...    ...     ...    ...
            3572      业(R)     87  文化艺术业  300144   宋城演艺
            3573      业(R)     87  文化艺术业  300592   华凯创意
            3574      业(R)     87  文化艺术业  300640   德艺文创
            3575      业(R)     87  文化艺术业  600576   祥源文化
            3576      业(R)     87  文化艺术业  603466    风语筑

    """

    result = {}
    if top <= 0:
        return result
    try:
        reader = _BaseReader('')
        page_index = 0
        while True:
            src = SRC
            if page_index > 0:
                src = urljoin(src, 'index_{0}.htm'.format(page_index))
            page_index = page_index + 1
            txt = _get_text(reader, src)
            dic = _parse_list(reader, txt)
            for key, value in dic.items():
                result[key] = value
                if len(result) >= top:
                    return result
    except RemoteDataError:
        pass
    finally:
        reader.close()
    return result


def _parse_list(reader, txt):
    """解析列表页面"""
    result = {}
    if txt:
        b = bs(txt, 'lxml')
        if b:
            ul = b.find('ul', attrs={'id': 'aaa'})
            if ul:
                alinks = ul.find_all('a')
                for link in alinks:
                    n = link.attrs['title']
                    if '上市公司行业分类结果' in n:
                        lk = _get_link(reader, link.attrs['href'], n)
                        if lk:
                            result[n] = lk
    return result


def _get_text(reader, src):
    """读取指定网页的内容"""

    rep = reader._get_response(src)
    if rep.ok:
        return str(reader._sanitize_response(rep), encoding='utf-8')
    return None


def _get_link(reader, src, text):
    u = urljoin(SRC, src)
    txt = _get_text(reader, u)
    if txt:
        b = bs(txt, 'lxml')
        if b:
            f = [a for a in b.find_all('a') if a.text == text]
            if f:
                return urljoin(u, f[0].attrs['href'])
    return None
