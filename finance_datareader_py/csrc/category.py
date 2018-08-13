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

    Returns:
         dict
        {文件名:pdf文件路径}

    Examples:
        .. code-block:: python

            >>> from finance_datareader_py.csrc import category

            >>> print(category.get_pdf())

            {
                "2018年2季度上市公司行业分类结果": "http://www.csrc.gov.cn/pub/newsite/scb/ssgshyfljg/201807/W020180730329934473366.pdf"
            }

    .. hint::
        对于 pdf 文件的解析，可以参考 `tabula-py <https://github.com/chezou/tabula-py>`_。

        .. code-block:: python

            >>> import tabula

            >>> df = tabula.read_pdf(r'http://www.csrc.gov.cn/pub/newsite/scb/ssgshyfljg/201805/W020180521522232342268.pdf',encoding='gbk', pages='all', format='json',silent=True, pandas_options={'header': 0})

            >>> df = df.loc[df['上市公司代码'].str.isnumeric() == True]

            >>> df = df.fillna(method='ffill')

            >>> print(df.tail())

                 门类名称及代码 行业大类代码 行业大类名称  上市公司代码 上市公司简称
            3597   综合(S)     90     综合  600777   新潮能源
            3598   综合(S)     90     综合  600783   鲁信创投
            3599   综合(S)     90     综合  600784   鲁银投资
            3600   综合(S)     90     综合  600805   悦达投资
            3601   综合(S)     90     综合  600895   张江高科

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
