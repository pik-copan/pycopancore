"""Port of MAGICC6.0 driven by an emissions scenario
"""
# This file is part of pycopancore.
#
# Copyright (C) 2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import base

from ..model_components import magicc6port as m

# entity types:

class World(m.World,
            base.World):
    """World entity type."""
    pass

# process taxa:

class Environment(m.Environment,
                  base.Environment):
    """Environment process taxon."""
    pass

class Model(m.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Port of MAGICC6.0 driven by an emissions scenario"
    """Name of the model"""
    description = "A simple/reduced complexity climate model, optionally driven by a MAGICC emissions scenario file in the format described in http://wiki.magicc.org/index.php?title=Creating_MAGICC_Scenario_Files"
    """Longer description"""

    entity_types = [World]
    """List of entity types used in the model"""

    process_taxa = [Environment]
    """List of process taxa used in the model"""
