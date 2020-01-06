Part 1. Overview and modularisation
-----------------------------------

Before actually starting the work, let us shortly get an overview of what needs 
to be done and understand the main structure of a model developed with 
copan:CORE.

Our model will have three **processes** ("things that happen"):

- *growth:* in each cell, a local resource stock grows, following the 
  continuous-time logistic growth model given by a certain ODE.

- *fishing:* each individual employs a certain effort to harvest the 
  resource growing in its cell, leading to individual catchs and an additional 
  fishing terms in the stock's ODE.
  
- *learning:* at random points in time given by a Poisson process,  
  each *i* in a random sample of individuals compares 
  her catch with that of randomly chosen acquaintance *j*,
  and copies *j*'s effort level with a probability depending on the difference 
  in catchs.

In pycopancore, the entities ("things that are") of a model are distinguished
by their **entity-type**. Of its four built-in entity-types, we only use two:

- ``Cell``, representing the place where a local resource stock is located 
  (corresponding to a *fish pond* in the Wiedermann paper),
- ``Individual``, representing a person fishing some local resource 
  (corresponding to a *fishing village* in the Wiedermann paper).

(Later on, we may also want to add some processes acting on the level of the
entity-types ``SocialSystem`` and ``World``, but we keep it simple for now.)

The main dynamic **variables** of the model will thus be

- ``Cell.fish_stock``
- ``Individual.fishing_effort``
- ``Individual.catch``: the catch

plus some fixed parameters which will also be treated as variables formally and 
introduced later.

To describe the relationships between cells and individuals, we make use of the 
following entity attributes shipped with copan:CORE's ``base`` model component:

- ``Individual.cell``: the home cell of the individual
- ``Cell.individuals``: list of all individuals living in the cell (in the 
  Wiedermann paper, only one fishing village has access to each fish pond, 
  but here we also allow several individuals to harvest in the same cell)
- ``Individual.culture``: the unique ``Culture`` process taxon relevant for all 
  individuals
- ``Culture.acquaintance_network``: the social network connecting the 
  individuals

In pycopancore, each variable and each process is *owned* by some object, 
most often an entity of a type such as ``Cell``, but sometimes by a so-called
*process taxon* such as ``Culture``. E.g., the inbuild ``acquaintance_network``
is owned not by any particular individual but by ``Culture`` itself, and 
individuals can access it via the *reference variable* named ``culture`` that
is owned by ``Individual``.

Since the three processes are only connected via the three variables and are 
otherwise independent, and since we may want to replace one of them by a 
different version later on (e.g., replace logistic growth by some other growth 
model or replace the particular form of social learning by some other form of 
learning), we will implement each process in its own model component and then 
plug them together to form the actual model.

So our **model components** will be

- **my_exploit_growth**: growth of ``Cell.fish_stock`` via an ODE

- **my_exploit_fishing**: computation of ``Individual.catch`` given 
  ``Individual.fishing_effort`` and corresponding reduction of 
  ``Cell.fish_stock`` via an ODE

- **my_exploit_learning**: for each ``Individual``, identify next time point 
  for learning, then, at that time point, draw a neighbour from 
  ``Culture.acquaintance_network``, compare own and neighbour's 
  ``catch`` and update own ``fishing_effort``.

Each model component will become a python subpackage of 
``pycopancore.model_components``, represented by a folder of the same name,
which mainly contains ... 

- a file ``model.py`` that defines which entity-types and process taxa the 
  component uses.

- a further subpackage called ``interface``that contains the 
  *interface classes* for all these entity-types and process taxa,
  describing what variables the component reads and writes;
  
- another subpackage called ``implementation`` that contains the 
  *implementation classes* for all these entity-types and process taxa,
  implementing the processes of the component. 
  
  
While the ``interface`` subpackage is typically represented by a single file 
``interface.py`` containing several short class definitions, the 
``implementation`` subpackage is typically represented by a subfolder 
``implementation`` that contains a separate file for each entity-type or 
process taxon with a single, longer class definition.

(Later on, when composing the actual model from the three model components, all 
classes contributing to the same entity-type will be *mixed* together via 
multiple inheritance, hence they will also be called *mixin* classes.)

In the **interface classes**, each variable is listed in one of three possible 
ways, each of which we will use for some variables:

- by reference to an existing variable definition from the *master data model*;
- by reference to an existing variable definition in another model component;
- by giving a new variable definition via instantiating the ``Variable`` class 
  and specifying all relevant meta-data for the variable.
  
In the **implementation classes**, we will implement the process logics using a 
number of different techniques suitable for different types of processes
(ODEs, algebraic equations, and rules for agent behaviour):

- the logistic growth ODE will be implemented in imperative-programming style 
  via a *method* of ``Cell`` that computes the RHS of the equation and stores 
  it in the special variable ``self.d_fish_stock``.

- the formula for the catch of all individuals in a cell will instead be given 
  in declarative-programming style by a simple *symbolic expression* 
  in the class ``Cell``, and the ODE for fishing will use the same expression.
  
- learning will be implemented via three methods, 
  one in ``Culture`` that returns the next time point for learning,
  another in ``Culture`` that selects the individuals that learn,
  and one in ``Individual`` that performs the actual learning.

We will see that there are often several alternative ways for implementing
a certain process and several alternative classes that could 'own' the process. 

(Although we need to implement the individual processes, we do *not* need to 
take care of how these equations get solved or when the different methods must 
be called, since that is the job of copan:CORE's inbuilt *runner*.)

After having implemented the three model components, we will compose from it 
the actual **model**. Just like model components are subpackages of 
``pycopancore.model_components``, a model is a subpackage of 
``pycopancore.models`` and is typically defined in a single python file inside 
the folder ``pycopancore/models``. The model definition will mainly import the 
necessary model components and will compose the final implementation classes of 
all entity-types and process taxa from the mixin classes provided by the 
components.

Finally, we will write a python script ``run_my_exploit.py`` that performs a 
simple **study** by running the model with some particular initial condition 
and parameter values and plotting some results. Such study scripts can be 
stored in the ``studies`` folder outside the pycopancore package.

Summarizing, we will first act as *model component developer*, then as 
*model composer*, and finally as *model end user*, and will eventually have 
written the following files (omitting certain secondary files we will learn 
about later)::

    pycopancore (repository folder)
    
      pycopancore (main package folder)
      | model_components
      | | my_exploit_growth
      | | | implementation
      | | | | cell.py
      | | | | environment.py
      | | | interface.py 
      | | | model.py
      | | my_exploit_fishing
      | | | implementation
      | | | | cell.py
      | | | | individual.py
      | | | | metabolism.py
      | | | interface.py 
      | | | model.py            
      | | my_exploit_learning
      | | | implementation
      | | | | culture.py
      | | | | individual.py
      | | | interface.py 
      | | | model.py            
      | models
      | | my_exploit.py
          
      studies (folder for studies)
      | run_my_exploit.py
      
Nicely, we can make use of some templates provided in the ``templates`` 
folder::

      templates (folder containing stuff to be copied and adjusted)
      | model_components
      | | SOME_COMPONENT (template for a model component folder)
      | | | ...
      | models
      | | SOME_MODEL.py (template for a model)
      | studies
      | | SOME_STUDY.py (template for a study)
      
So, let's go: :doc:`first_component`
