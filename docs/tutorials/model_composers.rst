Model composers
===============

*Model composers* create new models by arraging existing model components
provided by :doc:`model component developers <./model_component_developers>`.

This is done by creating a python file in that used entity types, process taxa
and model components are arranged.

For the exemplary seven dwarfs model the following file was created:


::

    #
    # Imports
    #

    from .. import base # all models must use the base component

    from ..model_components import seven_dwarfs as sd


    # entity types:

    class World(sd.World,
                base.World):
        """World entity type."""

        pass


    class Cell(sd.Cell,
               base.Cell):
        """Cell entity type."""

        pass


    class Individual(sd.Individual,
                     base.Individual):
        """Individual entity type."""

        pass


    # process taxa:

    class Culture(sd.Culture,
                  base.Culture):
        """Culture process taxon."""

        pass


    # Model class:

    class Model(sd.Model,
                base.Model):
        """Class representing the whole model."""

        name = "Seven dwarfs"
        description = "Tutorial model"
        entity_types = [World, Cell, Individual]
        """List of entity types used in the model"""
        process_taxa = [Culture]
        """List of process taxa used in the model"""

