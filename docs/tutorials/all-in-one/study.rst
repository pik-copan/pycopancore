Part 6: Using the model for a study
-----------------------------------

As we have seen, model components and models are implemented in an 
*object-oriented* way as subpackages and modules of the ``pycopancore`` 
*package* folder. Studies that use a model for a simulation experiment are
however implemented as python *scripts* and reside in the ``study`` folder.
So let us now switch into the role of a *model end user* and perform some such
'study'. Again, we can use a template to get started:

- Copy ``templates/studies/SOME_STUDY.py`` to ``studies/run_my_exploit.py`` and
  edit the imports like this::
  
    import pycopancore.models.my_exploit as M 

- In this study, we have only one social system and allow our individuals to 
  have only two possible ``fishing_efforts``, hence we adjust the parameters 
  as follows::

    # model parameters:
    
    ncells = 100
    nindseach = 1  # no. of individuals per cell
    link_density = 0.1  # random network link density
    low_effort = 30 * D.person_hours / D.weeks
    high_effort = 60 * D.person_hours / D.weeks
    
    # simulation parameters:
    
    t_max = 100  # interval for which the model will be simulated
    dt = 1  # desired temporal resolution of the resulting output.

- Adjust the entity generation as follows::
    
    world = M.World(environment = env, metabolism = met, culture = cul)
    soc = M.SocialSystem(world = world)
    cells = [M.Cell(social_system = soc) for j in range(ncells)]
    inds = [M.Individual(cell = c,
                fishing_effort = choice([low_effort, high_effort])
                ) for c in cells for j in range(nindseach)]

Note how we have already set all individuals' initial fishing effort here.
Another possibility for setting initial values for a whole list of entities
at the same time is by using the ``set_values`` method of the corresponding
``Variable`` object in the entity-type's class. Let's do this for the initial
fish stocks:

- Replace the random population block by this similar code::
    
    S0 = uniform(size=ncells)
    M.Cell.fish_stock.set_values(cells, S0)
    
Note that here we did not specify a unit, so the numbers will be interpreted as
multiples of the variable's default unit (``t_fish`` in this case, as specified
in the interface of ``my_exploit_growth``).

A third possibility to manipulate the initial value of a variable for some
specific entity or process taxon is by accessing the variable's *value*
directly, so we could have instead written::

    for c in cells:
        c.fish_stock = uniform() * M.t_fish

We use this way of accessing values now for initializing the social network
between the individuals, which is stored in the variable 
``Culture.acquaintance_network``. Since this is shipped with the ``base``
component of pycopancore, it was automatically initialized to contain an empty
network when ``Culture`` was instantiated above. Likewise, each ``Individual``
that was generated above has already registered itself automatically as a node
of this network. So the only thing that remains for us to do is add some links.
Since this is a common task, the template already contains suitable code for
this::

    # initialize some network:
    for index, i in enumerate(inds):
        for j in inds[:index]:
            if uniform() < link_density:
                cul.acquaintance_network.add_edge(i, j)

The subsequent code block eventually runs the model, and we can also leave it
as it is::

    runner = Runner(model=model)
    traj = runner.run(t_0=0, t_1=t_max, dt=dt)

After this simulation has finished, the ``traj`` object returned by 
``Runner.run()`` contains the time evolution of all variables from ``t_0``
to ``t_1`` in steps which are *at most* ``dt`` apart. The actual time steps
might vary since our model has irregularly timed events at completely random 
time points and the runner returns all event time points plus sufficiently 
many intermediate time points.
Since at event time points some variables will display discontinuous behaviour, 
the runner actually returns *two* entries for each such event time point *t*
(but not for the intermediate time points), the first containing the variable 
values *right before t*, the second those *right after t*.

The precise data structure of ``traj`` is this:

- ``traj['t']`` is the list of reported time points
- ``traj[M.Cell.fish_stock][c]`` is the list of corresponding fish 
  stocks of cell ``c``.

Hence if we want the total fish stock and average fishing effort plotted as 
the final step of our study, we can do it like this:

- Adjust the final plotting code as follows:: 

    stock = traj[M.Cell.fish_stock]
    effort = traj[M.Individual.fishing_effort] 
    total_stock = np.sum([stock[c] for c in cells], axis=0)
    avg_effort = np.mean([effort[i] for i in inds], axis=0)
    plt.plot(traj["t"], total_stock, 'g', label="fish stock")
    plt.plot(traj["t"], avg_effort, 'b', label="fishing effort")
    plt.legend()
    plt.show()

This finishes our coding work, so let's finally try it out and hope we made no
typos: :doc:`test`

