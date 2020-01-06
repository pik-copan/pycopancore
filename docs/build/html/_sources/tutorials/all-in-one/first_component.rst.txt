Part 2. Implementing the growth component
-----------------------------------------

From parts 2 to 4, we act in the role of a *model component developer*.
We start by doing some simple preparations:

- ``git clone https://github.com/pik-copan/pycopancore.git``

- ``cd pycopancore``

- ``cp -r templates/model_components/SOME_COMPONENT pycopancore/model_components/my_exploit_growth``

- In the copied subfolder ``implementation``, we delete those files we won't 
  need since they belong to entity-types and process taxa that we don't use in 
  this component: ``culture.py``, ``individual.py``, ``metabolism.py``, 
  ``social_system.py``, ``world.py``.

- We also remove the corresponding imports from ``implementation/__init__.py``, 
  keeping only these two imports::
  
    from .cell import Cell

    from .environment import Environment
  
- Similarly, in ``model.py``, we follow the ``# TODO:`` comments and delete the 
  unneeded imports and list entries, so that it basically contains this code 
  (plus comments and docstrings omitted here)::
  
    from . import interface as I
    from .implementation import Cell
    from .implementation import Environment   
    
    class Model (I.Model):
        entity_types = [Cell]
        process_taxa = [Environment]

Now the actual work begins by writing the component's **interface**, 
so open ``interface.py`` and do the following:

- In ``class Model``, 
  fill in a name and description for the component, like::
  
    name = "my exploit: growth"
    description = "growth component of the exploit tutorial model"

- Delete the class definitions of all unused entity-types and process taxa, 
  only keeping those of ``Cell`` and ``Environment``.
  
In ``class Cell``, we need to define the variable ``fish_stock``. Since it is 
a metaphorical variable representing a not further specified type of resource 
we just call ``fish`` for convenience, we should *not* use any of the existing 
specific stock variables from the master data model, such as 
``terrestrial_carbon_stock``, but we should define it as a new variable owned 
by this component. Still, we are thorough and give it an appropriate physical 
dimension (``fish``) and unit (``t_fish``), so that it gets not mixed up with 
other quantities in ways that make no sense. Therefore:

- Add in the header::

    from ...data_model import Dimension, Unit

- and in ``class Model``::
    
    class Model...
        ...
        fish = Dimension("fish", # name
                         "mass of fish") # description
        fish.default_unit = t_fish = \
            Unit("t fish", "metric tonnes of fish", symbol="t")
    
- Uncomment the lines::

    from ... import Variable
    
    PERSONALCELLVARIABLE = Variable(...
    
- Edit the latter to read::

    fish_stock = Variable(
        "fish stock",
        "stock of a generic local resource 'fish' that can grow and be harvested",
        unit = Model.t_fish,
        lower_bound = 0,
        is_extensive = True)

The names given as the first arguments of ``Dimension``, ``Unit`` and 
``Variable`` will be used in labels and log, while the descriptions given next 
appear in the automatically generated API documentation and are mainly intended 
as documentation for other users. We state that the stock cannot get negative,
and by saying ``is_extensive = True`` we state that this is a physically 
extensive quantity, i.e., that it is meaningful to add up resource stocks of 
different cells, e.g., to report the total stock. (We will encounter 
non-extensive quantities later, and in the API documentation of ``Variable``, 
further possible metadata are described.)

We will add further variables here later whenever we need them, so best keep 
``interface.py`` open. We turn to the **implementation** now by opening 
``implementation/cell.py``. Here, we will implement the logistic growth of 
``fish_stock``, which we could do either via a method or a symbolic expression.
We chose to do it by specifying the corresponding term in the ODE for 
``fish_stock`` via a *method* of ``Cell``:

- In ``implementation/cell.py``, add this import::

    from .... import ODE

- Add the following method to ``class Cell``::

    def grow(self, unused_t):
        competition_factor = 1 - self.fish_stock / self.fish_capacity
        growth_rate = self.environment.basic_fish_growth_rate * competition_factor
        self.d_fish_stock += growth_rate * self.fish_stock
  
- In the list ``processes = []``, add the following list entry::

    ODE("fish growth", [I.Cell.fish_stock], grow)

Any process declaration is of the form 
``PROCESS_TYPE("NAME", [TARGET_VARIABLE(S)], ...)``,
where ``PROCESS_TYPE`` can be ``ODE``, ``Explicit``, ``Event``, etc.,
and each ``TARGET_VARIABLE`` is a ``Variable`` object referenced via the 
interface ``I``.
With the process entry, we declare that ``fish_stock`` changes according to an
ordinary differential equation and that the method ``grow`` adds a term to this 
differential equation. Note that the method does so not by *returning* the term 
but by explicitly adding it to the special attribute ``Cell.d_fish_stock`` 
which represents the time derivative of ``Cell.fish_stock``. Note also that we 
only *add* (``+=``) to ``Cell.d_fish_stock`` rather than overriding its value 
(``=``), since other processes may want to add further terms to the same ODE
(and indeed we will do so later ourselves!).

When running the model, pycopancore will automatically call this method from 
within its ODE solver, giving it the current model time as the only argument. 
Since our ODE is time-independent, we don't make use of that argument and hence 
name it ``unused_t`` to indicate this (otherwise we would have named it just 
``t``).

Since in ``grow``, we use two parameters, ``self.fish_capacity`` and 
``self.environment.basic_fish_growth_rate``, we need to specify them:

- In ``interface.py``, add::

    class Cell ...
    
        # exogenous variables / parameters:
        fish_capacity = Variable("fish capacity", 
            "limit to fish stock due to competition for resources",
            unit = Model.t_fish,
            lower_bound = 0,
            is_extensive = True,
            default = 1 * Model.t_fish)
            
    class Environment ...
    
        # exogenous variables / parameters:
        basic_fish_growth_rate = Variable("basic fish growth rate",
            "basic rate at which fish would grow without competition",
            unit = D.months**(-1),
            lower_bound = 0,
            is_intensive = True,
            default = 2 / D.years)
            
While we treat the capacity as a cell variable that may vary from cell to cell,
we treat the basic growth rate as some kind of natural constant which belongs
to the environment rather than a particular cell, and we access it in the 
method ``grow`` via the inbuilt reference variable ``environment`` of 
``Cell`` by writing ``self.environment.basic_fish_growth_rate``.

Note that growth rates are *intensive* (rather than extensive), which means 
that they do not add up when adding stocks, but would rather lead to some kind 
of effective rate that could be computed by averaging the individual rates in 
an appropriate way.

For parameters, one often wants to specify default values, which we have done 
here. Bounds and default values can either be specified as pure numbers (like 
``0``), in which case they are assumed to be in the unit specified under 
``unit=``, or as *dimensional quantities* (like ``2 / years``, 
meaning two per year), in which case the unit of the dimensional 
quantity must belong to the same physical dimension as the unit specified under 
``unit=``. In the latter case, pycopancore automatically takes care of the 
necessary conversions, hence we encourage you to always specify values in the 
units your source data provides in order to make them more easily verifiable 
for the reader and avoid conversion mistakes.

As you can see, units can also be multiplied and divided to create suitable 
units for derived dimensions. E.g., in the case of ``basic_fish_growth_rate``, 
the correct dimension is fish per time, so we can use units such as 
``years**(-1)``, ``months**(-1)``, etc. We don't need to define the 
time dimension and units ourselves but use those provided by pycopancore's 
*master data model*, which is here imported under the abbreviation ``D``
(more on this later).

Note that when working with units and dimensional quantities, some *caution* is 
necessary: pycopancore distinguishes between *units* such as metres, seconds, 
tonnes, etc., and *dimensional quantities* such as 'one metre', 'two seconds', 
'half a tonne', etc. Values of variables, including bounds and default values,
must be of type ``DimensionalQuantity`` and can be generated by multiplying 
an object of type ``Unit`` (such as ``seconds``) with a number *from the left*,
e.g., ``2 * D.seconds`` (two seconds), or dividing a number by a unit, e.g., 
``50 / D.seconds`` (fifty Hertz). So ``D.metres`` is the length unit of metres, 
while ``1 * D.metres`` is the dimensional quantity of one metre, which is 
identical to ``.001 * D.kilometers``. However, since we also want to be able to 
derive larger from smaller units, multiplying a unit with a number from the 
*right*, or dividing a unit by a number, gives a new ``Unit`` rather than a 
dimensional quantity. Indeed, ``D.kilometers`` is defined in the master data 
model basically as ``kilometers = meters * 1000``. Hence, the dimensional 
quantity 'half a kilogram' must be written ``0.5 * D.kilograms``, while the 
German unit 'Pfund' ('half-kilograms') could be defined as ``D.kilograms / 2``.
A typical mistake is to try specifying the unit of a rate as ``1 / D.years``,
(which pycopancore interprets as the dimensional quantity of 'once per year'),
while the correct specification would be ``D.years ** (-1)``. Still, when you 
divide *two units* (rather than a number and a unit), you get a unit.
Hence it was correct for us to specify the unit of the base rate above as 
``t_fish / D.months`` (tonnes of fish per month).

To recap, in this part you've learned about...

- our code templates
- entity-types ``Cell``, ``Individual`` (more to follow)
- process taxon ``Environment`` (more to follow)
- interface vs. implementation classes
- ``Variable`` metadata (units, bounds, extensive quantities etc.)
- the process type ``ODE`` (more to follow)
- implementing processes via methods (see below for an alternative)
- details on dimensions, units, and dimensional quantities

Now that we have finished the first component, let's move on to the second:
:doc:`second_component`
