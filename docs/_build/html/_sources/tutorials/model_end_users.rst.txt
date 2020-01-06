Model end users
===============

A *model end user* runs a composed model, but changes neither model components nor the composition
of model components. The model end user only creates and works with the run file of the model.

If you want to know how to create your own model, read the :doc:`model composers <./model_composers>` tutorial. If you
want to know how to create new model components, read the
:doc:`model component developers <./model_component_developers>` tutorial.

Starting point for a *model end user* is the runfile template and the
:doc:`API documentation <../_api/pycopancore.models>` of the model at hand.
Using the documentation the *model end user* sets parameters, instantiates the necessary entities and taxa passing the
appropriate arguments and iterates the model using the runner. The output trajectory of the runner is ready for data
analysis and plotting.

This tutorial guides the reader through these steps using the
:doc:`seven dwarfs model <../_api/pycopancore.models~seven_dwarfs>`.

Starting point of the seven dwarf model: a fairy tale
-----------------------------------------------------
Once upon a time in a place far away seven dwarfs lived together in a cave.
Winter had come and they could not leave their cave to collect food. They grew
older and were to die, either from age or from hunger.

Their beards grew longer and the only thing giving them a glimpse of hope in
their pitiful lives was an old story of a beautiful princess that would arrive
some day and save them from their misery. When Snow White finally arrived she tricked them,
ate half of their food supplies and left them to die.

Creating a Runfile
------------------
This fairy tale was already transformed into the model components ``seven_dwarfs`` and ``snowwhite`` and
the composed model ``seven dwarfs``. Creating a copy of the template
runfile, we complete our runfile by executing the following steps.

Importing packages
------------------
At first, we import the necessary packages. Besides ordinary python packages needed for data analysis and plotting,
we import the seven dwarfs model from ``pycopancore.models`` and the runner from ``pycopancore.runners``.
::

    import numpy as np
    from time import time
    import datetime as dt

    import plotly.offline as py
    import plotly.graph_objs as go

    import pycopancore.models.seven_dwarfs as M
    from pycopancore.runners.runner import Runner


Setting of parameters
---------------------
Secondly, we set the parameters of our model, including the time interval of our simulation, the time step, the
number of dwarfs and the eating stock:
::

    # setting timeinterval for run method 'Runner.run()'
    timeinterval = 100
    # setting time step to hand to 'Runner.run()'
    timestep = .1
    nc = 1  # number of caves
    dwarfs = 7  # number of dwarfs

Instantiating Entities and Taxa
-------------------------------
Afterwards, we instantiate the model as well as its entities and taxa. In the seven dwarfs example, the entities
``World`` and ``Cell`` need some required keyword arguments. We collect these information by checking the entities and taxa in the
:doc:`API documentation <../_api/pycopancore.seven_dwarfs>`.
::

    model = M.Model()

    # instantiate process taxa culture:
    # In this certain case we need 'M.Culture()' for the acquaintance network.
    culture = M.Culture()

    # instantiate world:
    world = M.World(culture=culture)

    # instantiate cells (the caves)
    cell = [M.Cell(world=world,
                   eating_stock=100
                   )
            for c in range(nc)
            ]


Instantiating the Runner
------------------------
Upon instantiation of the runner, we need to pass the model object to the runner. It is possible to pass a list of
termination calls which comprise constraints defining under which circumstances the model run should stop. The
termination calls must be provided by an entity or a taxon of the model.
::

    start = time()

    print("done ({})".format(dt.timedelta(seconds=(time() - start))))

    print('\n runner starting')

    # Define termination signals as list [ signal_method, object_method_works_on ]
    # the termination method 'check_for_extinction' must return a boolean
    termination_signal = [M.Culture.check_for_extinction,
                          culture]

    # Define termination_callables as list of all signals
    termination_callables = [termination_signal]


    # Runner is instantiated
    r = Runner(model=model,
               termination_calls=termination_callables
               )


Simulating
----------
Now, all necessary objects required for a model run are instantiated. We set the start time and use the method ``run``
of the runner to start the simulation. The method returns the model trajectory as a python dictionary.
::

    start = time()
    # run the Runner and saving the return dict in traj
    traj = r.run(t_1=timeinterval, dt=timestep)
    runtime = dt.timedelta(seconds=(time() - start))
    print('runtime: {runtime}'.format(**locals()))

Analysing the Output and Plotting
---------------------------------
The structure of the trajectory is ``traj[M.Entity.Variable][Entity_number]`` and comprises a list of variable values
for every time step. The acquired data may be analysed and plotted.
