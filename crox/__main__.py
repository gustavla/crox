#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

import os
import sys
sys.path = [os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")] + sys.path
from crox.core import main

if __name__ == '__main__':
    main()
