"""Master data model for individual."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# from . import metabolism as MET
from . import culture as CUL


class Individual:

    is_environmentally_friendly = CUL.is_environmentally_friendly.copy()