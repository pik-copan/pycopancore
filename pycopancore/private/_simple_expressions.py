"""Created on Mar 20, 2017.

@author: heitzig
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# defines logics to deal with symbolic expressions and their evaluation


class _Unknown(object):

    def __str__(self):
        return "unknown"

    def update(self, *args):
        return self


unknown = _Unknown()


class _Unset(object):

    def __str__(self):
        return "unset"

    def update(self, *args):
        return self


unset = _Unset()
