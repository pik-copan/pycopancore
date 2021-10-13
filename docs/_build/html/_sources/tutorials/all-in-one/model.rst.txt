Part 5. Composing the model
---------------------------

Now that we have our three model components, we can switch from the role of a
*model component developer* into the role of a *model composer* and compose 
the three model components into an actual model:

- Copy ``templates/models/SOME_MODEL.py`` into ``pycopancore/models``, 
  rename it to ``my_exploit.py``, and edit it to have::
  
    from ..model_components import my_exploit_growth as growth
    from ..model_components import my_exploit_fishing as fishing
    from ..model_components import my_exploit_learning as learning

    ...
    
    class Cell(growth.Cell,
               fishing.Cell,
               base.Cell):
        """Cell entity type."""
        pass

Thereby you say which components the model has and which of them contribute to
the ``Cell`` entity type. The final ``Cell`` class is composed via multiple 
inheritance from the mixin classes provided by two of our model components,
and the basic ``Cell`` mixin class shipped within the ``base`` model component.
Note that ``base.Cell`` must always be named last in the list. (Despite this,
the order is almost arbitrary and matters only when different components
define the *same* attribute or method in different ways.)

- In the same way as for ``Cell``, edit the definitions of the classes 
  ``Individual``, ``Environment``, ``Metabolism``, and ``Culture``::
  
    class Individual(fishing.Individual,
                     learning.Individual,
                     base.Individual)...
                     
    class Environment(growth.Environment,
                      base.Environment)...
    
    class Metabolism(fishing.Metabolism,
                     base.Metabolism)...
                     
    class Culture(learning.Culture,
                  base.Culture)...
                  
- Even though we do not explicitly use them, all pycopancore models must also
  contain the ``World`` and ``SocialSystem`` entity-types, so we need to keep
  also::

    class World(base.World)...

    class SocialSystem(base.SocialSystem)...
  
The latter is because every ``Individual`` must belong to some ``SocialSystem`` 
and every ``Cell`` to some ``World``, hence we will have one object each of
those later on.

- Finally, also compose the ``Model`` class that will serve as the main 
  entry-point for pycopancore's runner, and edit its metadata::
  
    class Model(growth.Model,
                fishing.Model,
                learning.Model,
                base.Model):
        name = "exploit tutorial"
        description = "tutorial version of the copan:EXPLOIT model"
        entity_types = [World, SocialSystem, Cell, Individual]
        process_taxa = [Environment, Metabolism, Culture]

Now the model is ready to be used in a study: :doc:`study`
