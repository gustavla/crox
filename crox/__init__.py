from __future__ import print_function, division, absolute_import

from .core import defines


VERSION = (0, 1, 2)
ISRELEASED = True
__version__ = '{0}.{1}.{2}'.format(*VERSION)
if not ISRELEASED:
    __version__ += '.git'
