# -*- coding: utf-8 -*-
from __future__ import print_function
from ._version import __version__ as version

from . import presentation
from .presentation import Presentation

__author__ = "Dave Forgac, Ethan Swan"
__email__ = "eswan18@rocketmail.com"
__version__ = version


__all__ = ["presentation", "Presentation", "__author__", "__email__", "__version__"]
