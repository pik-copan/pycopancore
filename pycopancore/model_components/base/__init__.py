"""
This is the base model-component package,
also including internal framework logics (module model_logics)
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# export the interface:
from . import interface

# export all implementation classes:
from .implementation import *  # noqa: F403, F401

# export model component mixin class:
from .model import Model

__all__ = ["interface", "Model"]
