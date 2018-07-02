# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

from ._version import get_versions

__all__ = ['netease', 'sohu', 'sse', 'szse']

__version__ = get_versions()['version']
del get_versions
