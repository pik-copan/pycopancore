"""Culture process taxon mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
# from .... import master_data_model as D
# sure that's right?
from igraph import Graph


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    __background_proximity_network = None
    __interaction_network = None

    def __init__(self,
                 # *,  # TODO: uncomment when adding named args behind here
                 # degree_preference=None, agent_characteristics, social_influence, model_parameters (including number of individuals)
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)  # must be the first line
        # TODO: add custom code here:

        # exception
        #if not callable()

        # set intern variables

        self.n_individual = model_parameters.n_individual
        self.mean_degree_pref = model_parameters.mean_degree_pref
        self.std_degree_pref = model_parameters.std_degree_pref
        self.p_rew = model_parameters.p_rew

        # initiate contact network using degree preference
        # self.aquaintance_network = igraph.GraphBase.Erdos_Renyi(model_parametersn_individual, model_parameters.mean_degree_pref, directed=False)
        # WRONG! model component should provide structure, not detailed simulation

        self.__nodes = sortedlist(self.friendship_network.nodes())

        # initialise background proximity network
        __background_proximity_network = igraph.GraphBase.


        pass

    # process-related methods:


    def set_initial_conditions(self):

        # create background proximity
        #

        pass

    def generate_interaction_network(self):
        pass

    def update_social_influence(self):
        pass

    def update_contact_network(self):
        pass

    def one_step(self):
        pass



    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
