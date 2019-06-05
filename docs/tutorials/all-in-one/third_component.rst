Part 4. Implementing the learning component
-------------------------------------------

The third and last component we implement models in an agent-based fashion how 
individuals learn their ``fishing_effort`` from each other. Again, we use the
template to prepare the component, this time with a larger number of 
parameters:

- On the basis of the template, make another model component 
  ``model_components/my_expoit_learning``, this time only keeping the  
  entity-type ``Individual`` and the process taxon ``Culture``.

- In its ``interface.py``, uncomment and add the following imports and 
  variables::

    from ... import Variable
    from ... import master_data_model as D
    from ..my_exploit_fishing import interface as F

    class Individual...

        # endogenous:
        fishing_effort = F.Individual.fishing_effort    

        # exogenous:
        catch = F.Individual.catch
        
    class Culture...
    
        # endogenous:
        acquaintance_network = D.Culture.acquaintance_network
        
        # exogenous:
        fishing_update_rate = Variable("fishing effort update rate",
            """average number of time points per time where some individuals 
            update their fishing effort""",
            unit = D.years**(-1), default = 1 / D.years, lower_bound = 0)
        fishing_update_prob = Variable(
            "fishing effort update probability",
            """probability that an individual updates their fishing effort at
            an update time point""",
            default = 1/2, lower_bound = 0, upper_bound = 1)
        fishing_exploration_prob = Variable(
            "fishing effort exploration probability",
            """probability that an individual copies a neighbours effort if
            both catches are equal""",
            default = 0.1, lower_bound = 0, upper_bound = 1)
        fishing_imitation_char_prob = Variable(
            "fishing effort imitation characteristic probability",
            """probability that an individual copies a neighbours effort if
            the other's catch is twice the own catch""",
            default = 0.9, lower_bound = 0, upper_bound = 1)
            
The learning process consists of two parts: 

- With an average rate of
  ``fishing_update_rate``, an 'update time point' occurs in the ``Culture``.
  When that happens, each ``Individual`` (``self``) updates their fishing 
  effort with a probability of ``fishing_update_prob``. 
- If she updates, she draws a random neighbour of hers (``other``) from the 
  ``acquaintance_network``. Then she copies ``other``'s ``fishing_effort`` 
  with a probability ``imitation_prob(catch_ratio)``, where ``catch_ratio`` 
  equals ``other.catch / self.catch`` and the function ``imitation_prob``
  is sigmoid-shaped and monotonic and returns zero for ``catch_ratio == 0``, 
  ``fishing_exploration_prob`` iff ``catch_ratio == 1``, 
  ``fishing_imitation_char_prob`` iff ``catch_ratio == 2``
  and 1 for ``catch_ratio = np.inf``.
  
The first part we implement as follows, using the process type ``Event``:

- In ``implementation/culture.py``::

    from numpy.random import exponential, uniform
    from .... import Event
    from ...base import interface as B    
    
    class Culture...
    
        def next_fishing_update_time(self, t):
            return t + exponential(1 / self.fishing_update_rate)
            
        def update_fishing_efforts(self, unused_t):
            for w in self.worlds:
                for i in w.individuals:
                    if uniform() < self.fishing_update_prob:
                        i.update_fishing_effort()
                    
        processes = [
            Event("update fishing efforts",
                   [B.Culture.worlds.individuals.fishing_effort],
                   ["time",
                    next_fishing_update_time,
                    update_fishing_efforts])
        ]

An ``Event`` is something that happens at certain discrete time points. In our
case, its specification names two methods, one which returns the next time 
point at which the event happens (``next_fishing_update_time``), and one which
implements what happens at those time points (``update_fishing_efforts``).
The latter method finds out which individuals actually update and calls their
``update_fishing_effort`` method, which we will implement next:

- In ``implementation/individual.py``::

    from numpy import exp, log
    from numpy.random import choice, uniform

    class Individual...
    
        def fishing_imitation_prob(self, catch_ratio):
            offset = -log(1/self.culture.fishing_exploration_prob - 1)
            slope = -(log(1/self.culture.fishing_imitation_char_prob - 1) 
                      + offset) / log(2)
            return 1 / (1 + exp(- offset - slope*log(catch_ratio)))
        
        def update_fishing_effort(self):
            other = choice(list(
                self.culture.acquaintance_network.neighbors(self)))
            if uniform() < self.fishing_imitation_prob(other.catch / self.catch):
                self.fishing_effort = other.fishing_effort

As you see, the variable ``Culture.acquaintance_network`` that is provided in
the master data model, contains a network whose nodes are ``Individual`` s.
The data type of ``Culture.acquaintance_network`` is ``networkx.Graph``, as
you can see in the API documentation of the master data model
(:doc:`../../_api/pycopancore.data_model.master_data_model`), 
where it says:

    **acquaintance_network** = *variable 'acquaintance network' 
    (Basic undirected social network of acquaintance between Individuals. 
    Most other social networks will be subgraphs of this.),
    ref=https://en.wikipedia.org/wiki/Interpersonal_relationship#Stages, 
    not None, scale=nominal, datatype=\<class 'networkx.classes.graph.Graph'\>*

In this part you've learned about...

- using variables from the *master data model*
- the process type ``Event``
- using random value generators and networks

We're now ready to compose the three components into a model:
:doc:`model`
