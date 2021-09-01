# -*- coding: utf-8 -*-
from __future__ import print_function
from ._version import get_versions

from . import presentation
from .presentation import Presentation

__author__ = "Dave Forgac"
__email__ = "tylerdave@tylerdave.com"
__version__ = get_versions()["version"]
del get_versions


__all__ = ["presentation", "Presentation", "__author__", "__email__", "__version__"]
