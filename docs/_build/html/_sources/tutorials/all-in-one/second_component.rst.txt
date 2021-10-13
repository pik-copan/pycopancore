Part 3. Implementing the fishing component
------------------------------------------

In this part, we will add another component in which each cell uses
all corresponding individuals' fishing effort levels to determine 
their individual catchs and the decline of the fish stock.

- Just as before, copy the template to a new model component 
  ``model_components/my_expoit_fishing``, this time keeping only the following 
  entity-types and process taxa: ``Cell``, ``Individual``, ``Metabolism``.

- In its ``interface.py``, change the order of ``class Cell`` and 
  ``class Individual`` and uncomment and add the following imports and 
  variables::

    from ..my_exploit_growth import interface as G
    from ... import Variable
    
    class Individual...

        # endogenous:    
        catch = Variable("fishing catch", 
            "flow of fish received due to fishing",
            unit = G.Model.t_fish / D.months,
            lower_bound = 0,
            is_extensive = True)

        # exogenous:
        fishing_effort = Variable("fishing effort",
            "effort spent fishing",
            unit = D.person_hours / D.weeks,
            lower_bound = 0,
            is_extensive = True,
            default = 40 * D.person_hours / D.weeks)
            
    class Cell...
    
        # endogenous:
        fish_stock = G.Cell.fish_stock
        total_fishing_effort = Individual.fishing_effort.copy()
        total_catch = Individual.catch.copy()
        
    class Metabolism...
    
        # exogenous:
        catch_cost_coeff = Variable(
            "catch cost coeff.",
            """coefficient c of quadratic fishing cost function
            effort = c * catch**2""",
            unit = (D.person_hours / D.weeks) * D.years**2,
            lower_bound = 0,
            default = (40 * D.person_hours / D.weeks) / (1 / D.years)**2)  
                # so at 40 hrs per week, stock declines at rate 1/year

Several things can be learned from this:

- Different units of the same dimension work seemlessly together (like 
  ``years`` and ``weeks``).
  
- Derived units can be quite complex and can be specified as fractions which
  need not be reduced (pycopancore takes care of that automatically). E.g., 
  instead of the unit ``(D.person_hours / D.weeks) * D.years**2``)
  we could also have used ``D.persons * D.years**2`` 
  which would however be less transparent.
  
- If one component needs to access a Variable defined in another component,
  it needs to import the other component's interface and *use the same* 
  variable as seen in this line::
  
    fish_stock = G.Cell.fish_stock

- To define a *new* variable that has the same metadata as an existing one,
  e.g., since it is just an aggregation of the other variable to another 
  level, one can *copy* the other variable's *metadata* as seen in this line::

    total_fishing_effort = Individual.fishing_effort.copy()
    
- The latter only works here since we define ``Individual`` before ``Cell``,
  which is why we needed to change their order.

- The differences between referencing a variable and copying its metadata are:

    - When a component uses an existing variable, there is still just one 
      variable that both components have access to in order to exchange data. 
      Therefore, the variable must have the *same identifier* in all components
      that use it: ``fish_stock``.
      
    - When you copy a variable's metadata via ``copy()``, you get a new 
      variable that is totally independent of the original one and can have 
      *any identifier* you like. (If one wants one to be the aggregation of the
      other, one has to specify this relationship explicitly via an equation,
      see below for an example.)
      
We can now implement the fishing process, and this time we will specify the
corresponding equations not via methods but as symbolic expressions. The
catches of individuals fishing in the same cell will not be independent but 
will depend on the total effort of all individuals fishing in that cell, to 
reflect competition for best catch locations. Therefore, we model the process
as partially owned by the entity-type ``Individual`` and partially owned by the
entity-type ``Cell``. 

- In ``implementation/cell.py``, add some imports and three entries to the list of
  ``processes``::

    import sympy as sp  # to be able to use sp.sqrt
    from ...base import interface as B  # to be able to use B.Cell.metabolism
    from .... import Explicit, ODE

    class Cell...
    
        processes = [
            Explicit("total effort", 
                [I.Cell.total_fishing_effort],
                [B.Cell.sum.individuals.fishing_effort]),
            Explicit("total catch",
                [I.Cell.total_catch],
                [I.Cell.fish_stock
                 * sp.sqrt(I.Cell.total_fishing_effort
                           / B.Cell.metabolism.catch_cost_coeff)]),
            ODE("stock decline due to fishing",
                [I.Cell.fish_stock],
                [- I.Cell.total_catch])
        ]

Again, some things can be learned here:

- ODEs can either be specified via methods (as before) or via symbolic 
  expressions (as here). In the latter case, the third argument of the ``ODE``
  specification is not the name of a method but a list of symbolic expressions,
  one for each entry in the list of dependent variables (2nd argument of 
  ``ODE``). In our case, there's one dependent variable, ``I.Cell.fish_stock``,
  and one rather simple symbolic expression, ``-I.Cell.total_catch``.
  
- Similarly, processes that define some variables directly (rather than their 
  time derivative) as functions of some other variables are specified via the 
  process type ``Explicit``, and here again the third argument is either a 
  method that sets the dependent variables directly, or a list of symbolic 
  expressions. Above, we have said via a symbolic expression that 
  ``total_fishing_effort`` equals the sum of all the cell's individuals' 
  ``fishing_effort`` s. Alternatively, we could have specified the same as::
  
    import numpy as np
    
    class Cell...
    
        def total_effort (self, unused_t):
            self.total_fishing_effort = np.sum(
                [i.fishing_effort for i in self.individuals])
                
        processes = [
            Explicit("total effort", 
                [I.Cell.total_fishing_effort],
                total_effort),
            ...
        ]
  
- Generally, a symbolic expression is basically a piece of code constructed 
  from these possible ingredients:
  
  - Variables defined in an interface such as ``I.Cell.total_catch``
  - Variables of other entity-types or process taxa (e.g. 
    ``Metabolism.catch_cost_coeff``) accessed via an inbuilt reference variable
    defined in the base component (e.g. ``B.Cell.metabolism``),
    leading to a so-called *dot-construct* such as 
    ``B.Cell.metabolism.catch_cost_coeff``.
  - Aggregation keywords specified as part of a dot-construct, such as ``sum``
    in ``B.Cell.sum.individuals.fishing_effort``. Valid aggregations for
    numerical variables are ``sum``, ``mean``, ``median``, ``min``, ``max``, 
    ``std`` and ``var``, and the aggregation keyword must be followed by a
    set-valued reference variable such as ``individuals``, ``cells``, etc.
  - Mathematical functions provided by the ``sympy`` package, such as 
    ``sp.sqrt``. (Caution: do *not* use ``numpy`` functions in symbolic expr.!)
  - Standard operators and numerals such as ``+``, ``**``, ``12.345`` etc.
    
We complete the implementation of the fishing component like this:

- In ``implementation/individual.py``, add::

    from ...base import interface as B
    from .... import Explicit
    
    class Individual...
    
        processes = [
            Explicit("individual catch",
                [I.Individual.catch],
                [B.Individual.cell.total_catch 
                 * I.Individual.fishing_effort 
                 / B.Individual.cell.total_fishing_effort])
        ]
        
(Note that alternatively, we could have achieved the same effect by letting
``Cell`` own this part of the process as well::

    class Cell...
    
        processes = [
            ...
            Explicit("individual catch",
                [B.Cell.individuals.catch],
                [I.Cell.total_catch 
                 * B.Cell.individuals.fishing_effort 
                 / I.Cell.total_fishing_effort])
        ]

In this version, each cell 'hands out' the catch to all its corresponding
individuals, so the target variable reads ``B.Cell.individuals.catch``
instead of ``I.Individual.catch``. If you compare the two versions, you will
notice that in the first version, all occurring variables and dot-constructs
start with ``Individual``, while in the second they all start with ``Cell``.
As a general rule, all variables and dot-constructs occurring in a process
owned by some entity-type process taxon must start with that entity-type or
process taxon and can access other entity-types' or process taxons' variables
only via reference variables.)

To recap, in this part you've learned about...

- process taxon ``Metabolism``
- some predefined time units, and using several units simultaneously 
- using variables defined in other components
- copying metadata from existing variables to new variables
- the process type ``Explicit``
- implementing processes via symbolic expressions
- reference variables, dot-constructs, and aggregation keywords

Let's move on to the last component: :doc:`third_component`
