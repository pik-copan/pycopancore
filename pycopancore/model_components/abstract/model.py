"""Abstract Model component class, inherited by base component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


class Model (object):
    """Abstract Model component class, inherited by base component."""

    # class attributes later holding the specific model component's metadata:

    name = None  # a unique name for the model component
    description = None  # some description
    # list of other model components required for this model component
    # to make sense:
    requires = None

    # Lists of mixin classes contributed by this component:

    entity_types = None
    process_taxa = None
