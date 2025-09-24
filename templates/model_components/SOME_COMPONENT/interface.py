"""model component Interface template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Use variables from the master data model wherever possible
from ... import master_data_model as D

# TODO: uncomment and adjust to use variables from other pycopancore model
# components:
# from ..MODEL_COMPONENT import interface as MODEL_COMPONENT

# TODO: uncomment and adjust only if you really need other variables:
# from ... import Variable


class Model(object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """a unique name for the model component"""
    description = "..."
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


#
# Entity types
#
class World(object):
    """Interface for World mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEWORLDVARIABLE = D.World.ONEWORLDVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERWORLDVARIABLE= MODEL_COMPONENT.World.ANOTHERWORLDVARIABLE

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALWORLDVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:
    # TODO: similarly


class SocialSystem(object):
    """Interface for SocialSystem entity type mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONESOCIALSYSTEMVARIABLE = master_data_model.SocialSystem.ASOCIALSYSTEMVAR

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERSOCIALSYSTEMVARIABLE = (
    # MODEL_COMPONENT.SocialSystem.MORESOCIALSYSTEMVARIABLE
    # )

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALSOCIALSYSTEMVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


class Cell(object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONECELLVARIABLE = master_data_model.Cell.ONECELLVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERCELLVARIABLE= MODEL_COMPONENT.Cell.ANOTHERCELLVARIABLE

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALCELLVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


class Individual(object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEINDIVIDUALVARIABLE = master_data_model.Individual.ONEINDIVIDUALVAR

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERINDIVIDUALVARIABLE= MODEL_COMPONENT.Individual.MOREINDIVIDUALVAR

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALINDIVIDUALVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


#
# Process taxa
#
class Environment(object):
    """Interface for Environment process taxon mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEENVIRONMENTVARIABLE = master_data_model.Environment.ONEENVIRONMENTVAR

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERENVIROMENTVARIABLE= MODEL_COMPONENT.Environment.MORENVIROMENTVAR

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALENVIROMENTVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


class Metabolism(object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEMETABOLISMVARIABLE = master_data_model.Metabolism.ONEMETABOLISMVAR

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERMETABOLISMVARIABLE= MODEL_COMPONENT.Metabolism.MOREMETABOLISMVAR

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALMETABOLISMVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


class Culture(object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONECULTUREVARIABLE = master_data_model.Culture.ONECULTUREVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERCULTUREVARIABLE= MODEL_COMPONENT.Culture.ANOTHERCULTUREVARIABLE

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALCULTUREVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:
