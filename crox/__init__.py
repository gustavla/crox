from __future__ import print_function, division, absolute_import


VERSION = (0, 0, 1)
ISRELEASED = False
__version__ = '{0}.{1}.{2}'.format(*VERSION)
if not ISRELEASED:
    __version__ += '.git'
