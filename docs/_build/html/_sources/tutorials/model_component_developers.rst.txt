Model component developers
==========================

A *model component developer* develops new components in order to provide novel features for a model.

This tutorial guides the reader through the implementation of a
new model component using the ``seven dwarfs model`` as an example.

Developing a new model component
--------------------------------

At first,

Entities and process taxonomy
-----------------------------

Determine necessary
:doc:`entity types<../framework_documentation/entity_types/index>` and
:doc:`process taxa <../framework_documentation/process_taxonomy/index>`

Create model component files from template
------------------------------------------

Copy necessary template files. The structure of a model component is explained
:doc:`here <../framework_documentation/python_implementation/model_components>`.


Create attributes and methods of entites and taxa
-------------------------------------------------



Code snippet 1 from ``culture.py``:

::

    class Culture (I.Culture):
        """Culture process taxon mixin for exploit_social_learning."""

        # standard methods:

        def __init__(self,
                     *,
                     last_execution_time=None,
                     **kwargs):
            """Initialize the unique instance of Culture."""
            super().__init__(**kwargs)
            self.last_execution_time = last_execution_time
            self.consensus = False

        # process-related methods:

        def social_update(self, t):
            """Execute the social update.

            Parameters
            ----------
            t : float
                time

            Returns
            -------

            """
            ...


        def reconnect(self, agent_i, agent_j):
            """Reconnect agent_i from agent_j and connect it to k.

            Disconnect agent_i from agent_j and connect agent_i
            to a randomly chosen agent_k with the same strategy,
            agent_i.strategy == agent_k.strategy.

            Parameters
            ----------
            agent_i : Agent (Individual or SocialSystem)
            agent_j : Agent (Individual or SocialSystem)

            Returns
            -------

            """
            ...


        def change_strategy(self, agent_i, agent_j):
            """Change strategy of agent_i to agent_j's.

            Change the strategy of agent_i to the strategy of agent_j
            depending on their respective harvest rates and the imitation tendency
            according to a sigmoidal function.

            Parameters
            ----------
            agent_i : Agent (Individual or SocialSystem)
                Agent i whose strategy is to be changed to agent j's strategy
            agent_j : Agent (Individual or SocialSystem)
                Agent j whose strategy is imitated
            Returns
            -------

            """
            ...


        def get_update_agent(self):
            """Return the agent with the closest waiting time.

            Choose from all agents the one with the smallest update_time.
            Returns
            -------

            """
            ...


        def set_new_update_time(self, agent):
            """Set next time step when agent is to be called again.

            Set the attribute update_time of agent to
            old_update_time + new_update_time, where new_update_time is again
            drawn from an exponential distribution.

            Parameters
            ----------
            agent : Agent (Individual or SocialSystem)
                The agent whose new update_time should be drawn and set.

            Returns
            -------

            """
            ...


        def check_for_consensus(self):
            """Check if the model has run into a consensus state.

            The model is in a consensus state if in each connected component
            all agents use the same strategy. In this case, there will be no more
            change of strategies since the agents are only connected to agents
            with the same strategy.

            Returns
            -------
            consensus : bool
                True if model is into consensus state, otherwise False
            """
           ...


        def step_timing(self,
                        t):
            """Return the next time step is to be called.

            This function is used to get to know when the step function is
            to be called.
            Parameters
            ----------
            t : float
                time

            Returns
            -------

            """
           ...



Specifying processes
--------------------

At the end of the taxon file, the relevant
:doc:`processes <../framework_documentation/process_types/index>`
need to be specified.

In the EXPLOIT example, there is only one process implemented in the culture
taxon. It is a ``step`` process which incorporates one update:
::

    processes = [Step('Social Update is a step function',
                      [I.Culture.acquaintance_network,
                       I.Individual.strategy, I.Individual.update_time,
                       I.Culture.consensus],
                      [step_timing, social_update])]



Import ./implementation files in ``model.py`` file.


Adjusting interface file and model file
---------------------------------------

::

    # entity types:
    class World(object):
    """Define Interface for World."""

    contact_network = Variable('contact network', 'network')
    agent_list = Variable('list of all agents', 'all agents in network')






Module testing
--------------

