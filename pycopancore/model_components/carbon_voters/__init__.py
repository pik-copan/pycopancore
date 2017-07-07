"""
Model component package template.

TODO:
Copy this folder, rename it to the name of your model component,
then adjust or fill in code and documentation in all modules wherever marked by "TODO:",
finally remove these instructions.
See the model component development tutorial for details.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from . import interface

# export all implementation classes:
from .implementation import *

# export model component mixin class:
from .model import Model
