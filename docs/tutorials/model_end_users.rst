Model end users
===============

A model end user is a person who runs a composed model, but changes neither model components nor the composition
of model components. The model end user only works with the run file of the model.

If you want to know how to create your own model, read the :doc:`model composers <./model_composers>` tutorial. If you
want to know how to create new model components, read the :doc:`model component developers <./model_component_developers>`
tutorial.

Starting point of model example: a fairy tale - UPDATE NEEDED
-------------------------------------------------------------
Once upon a time in a place far away seven dwarfs lived together in a cave.
Winter had come and they could not leave their cave to collect food. They grew
older and were to die, either from age or from hunger.

Their beards grew longer and the only thing giving them a glimpse of hope in
their pitiful lives was an old story of a beautiful princess that would arrive
some day and save them from their misery. When Snow White had finally arrived they
discovered she tricked them, ate half of their food supplies and left them
to die.

Runfile
-------
A model end user only uses the run file provided by the model composer. It is not necessary to understand the model
composition or the individual packages for being a model end user. However, understanding the run file is crucial for
running a simulation and changing parameters.

Import of packages
------------------
At first, we import necessary packages. Besides ordinary python packages, we import the seven dwarfs model from
``pycopancore.models`` and the runner from ``pycopancore.runners``.

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
Secondly, we set the parameters of our model, including the time interval, the time step, the number of dwarfs,
the eating stock ...
::

    # setting timeinterval for run method 'Runner.run()'
    timeinterval = 100
    # setting time step to hand to 'Runner.run()'
    timestep = .1
    nc = 1  # number of caves
    dwarfs = 7  # number of dwarfs

Instantiation of Entities and Taxa
----------------------------------

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
wc

Runner instantiation
--------------------
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
wwcw

Simulation
----------
::

    start = time()
    # run the Runner and saving the return dict in traj
    traj = r.run(t_1=timeinterval, dt=timestep)
    runtime = dt.timedelta(seconds=(time() - start))
    print('runtime: {runtime}'.format(**locals()))

    # saving time values to t
    t = np.array(traj['t'])
    print("max. time step", (t[1:]-t[:-1]).max())


Plotting
--------
trajectory files