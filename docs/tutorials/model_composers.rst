Model composers
===============

*Model composers* create new models by arraging existing model components
provided by :doc:`model component developers <./model_component_developers>`.
This is done by creating a python file in that used *entity types*, *process taxa*
and *model components* are arranged in inheriting classes.
The basic structure of this file can be examined in the *_template* directory of this package.

In the following a step-by-step tutorial, based on the exemplary
:doc:`seven dwarfs toy model <../_api/pycopancore.models>`, is provided.

The general workflow
is  structured as follows:

(1) Import of desired model components
(2) Setting entity types and process taxa
(3) Composing the model class


1. Import of model components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *base model component*
is used in every model and its import is therefore mandatory.

Besides, additional components can be included. In case of the
:doc:`seven dwarfs toy model <../_api/pycopancore.models>`
the *seven_dwarfs* as well as *snowwhite* components are used.
::

    from .. import base

    # additional components
    from ..model_components import seven_dwarfs as sd
    from ..model_components import snowwhite as sw





2. Setting entity types and process taxa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this step *entity types* and *process taxa* are arranged. This is done by basic python
inheritance. Note that primary inheritors will overwrite attributes of secondary ones.

::

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


3. Composing the model class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model class is composed by putting all model classes together.
As above this is done by inheritance. Further one needs to specify
entity types and process taxa that are used in the model. 

The Model class for the :doc:`seven dwarfs toy model <../_api/pycopancore.models>`
is set up as follows:

::

    class Model(sd.Model,
                base.Model):
        """Class representing the whole model."""

        name = "Seven dwarfs"
        description = "Tutorial model"
        entity_types = [World, Cell, Individual]
        """List of entity types used in the model"""
        process_taxa = [Culture]
        """List of process taxa used in the model"""

Here entity types *World*, *Cell* and *Individual* as well as
the process taxa *Culture* are used. 

