Model composers
===============

A *model composer* creates new models by arraging existing model components
provided by :doc:`model component developers <./model_component_developers>`.

This is done by creating a python file in that used *entity types*, *process taxa*
and *model components* (TODO reference) are arranged in inheriting classes.

The basic structure of this file can be examined in the *_template* (reference TODO).

In the following a step-by-step tutorial, based on the exemplary
:doc:`seven dwarfs model <../_api/pycopancore.models>`, is provided.

Import of model components
~~~~~~~~~~~~~~~~~~~~~~~~~~
All components that are used must be imported. The *base model component* (reference TODO)
is used in every model and its import therefore mandatory.

Besides that, additional components can be included. In case of the *seven dwarfs model* (TODO reference)
the *seven_dwarfs* as well as *snowwhite* components are used.
::


    # base import (always needed)
    from .. import base

    # additional components
    from ..model_components import seven_dwarfs as sd
    from ..model_components import snowwhite as sw





Arrangement of entity types and process taxa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this step *entity types* and *process taxa* are arranged. This is done by basic python
inheritance. Note that primary inheritors will overwrite attributes of secondary ones (TODO better formulation).

::
=======
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


The model class
~~~~~~~~~~~~~~~

This arrangement puts all model classes together. (TODO)




