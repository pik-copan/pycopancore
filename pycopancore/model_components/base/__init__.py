"""
This is the base model-component package, 
also including internal framework logics (module model_logics)
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# export the interface:
from . import interface

# export all implementation classes:
from .implementation import *

# export model component mixin class:
from .model import Model
