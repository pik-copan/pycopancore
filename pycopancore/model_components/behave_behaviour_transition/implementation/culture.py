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
import numpy as np
import igraph
import networkx as nx
import scipy


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:


    # The Kolmogorov-Smirnov-Test should be done in the run file for several reasons:
    # 1. It is a method connected to the exogenous agent characterics, namely the agent's disposition
    # 2. An array of characteristics is produced in the run file (sure about that?), hence it should be placed there.
    # TODO BUT: Maybe the model component should provide this test since it is essential for the BEHAVE model.
    # TODO: Should more parameters be passed on to the function?
    def __kolmogorov_smirnov_test(self, current_distribution, target_distribution):
        """
       This function governs the transition between two distributions.

       The functions' similarity is derived via a Kolmogorov-Smirnov test
       as a necessary criterium
       (https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).

       The target is set to 0.1, which is equivalent to the value one gets
       for random sampling from the given distribution.

       The noise added is lognormal distributed to allow for
       long-range jumps and scaled with the deviation of the actual distribution
       to the ideal curve. The greater the positive deviation, the greater the
       noise.
       """

        kolm_smir_step = 2

        # Kolm Smir target
        target = 0.1
        # noise scaling coeff
        tr_noise_coeff = 0.1

        # set counters
        k = 1
        n_inc = 0

        # TODO: LOOK AT THIS? DOES THE K_S_TEST NEED THIS FUNCTION? HOW CAN I DO THIS SMARTER?
        #  Define helper function
        def integrate_cdf(input_array):
            cdf = np.zeros(input_array.shape[0])
            for i in range(input_array.shape[0]):
                cdf[i] = integ.quad(lambda x: distribution_function(yb, x),
                                    0, input_array[i])[0]
            return cdf

        # derive the ideal distribution for given yb
        hist_values_target, hist_bins_target = np.histogram(
            target_distribution, bins=100, range=(0, 1))
        # get deviation
        hist_values_current, hist_bins_current = np.histogram(
            current_distribution, bins=100, range=(0, 1))
        hist_values_current = np.append(hist_values_current, hist_values_current[-1])
        hist_diff = hist_values_current - hist_values_target
        # get the noise level for all N agents
        disp_distr_round = np.asarray(100 * current_distribution, dtype='int')
        distr_dev = hist_diff[disp_distr_round]
        distr_dev = np.asarray(distr_dev, dtype='float')
        # scale and set positive
        distr_dev = distr_dev / 50
        distr_dev += np.abs(distr_dev.min())
        logn_std = 1.
        while kolm_smir_step >= target:
            # generate random lognormal dist and sign
            random_noise_increase = np.random.lognormal(0, logn_std, N)
            random_sign = np.random.randint(-1, 1, N)
            random_sign[random_sign == 0] = 1
            # add the noise
            # TODO: WHAT IS THE ROLE OF distr_dev? Does it just provide some magnitude for the random shift?
            disp_distr_tp1 = (current_distribution + tr_noise_coeff * random_sign *
                              random_noise_increase * distr_dev)
            # TODO: CHANGE NAME OF DISP_DISTR_TPL
            # check for boundaries
            disp_distr_tp1[disp_distr_tp1 > 1] = current_distribution[disp_distr_tp1 > 1]
            disp_distr_tp1[disp_distr_tp1 < 0] = current_distribution[disp_distr_tp1 < 0]
            # Kolmogorov-Smirnov test
            kolm_smir_step = scipy.stats.kstest(disp_distr_tp1, integrate_cdf)[0]
            # print('kolm_smir_step',kolm_smir_step)
            k += 1
            # in case of non-convergence, increase the standard deviation for the
            # lognormal dist to allow for
            if k > 100:
                logn_std = logn_std * 1.2
                #print('increased noise, logn_std', logn_std)
                k = 1
                n_inc += 1
                if n_inc > 10:
                    print('DISTRIBUTION TRANSITION FAILED',
                          'kolm_smir_step', kolm_smir_step, 'yb', yb)
                    return current_distribution
        return disp_distr_tp1

        pass

        @staticmethod
        def __social_distance_smoker_function(agent_i, agent_j):
            """
            Returns social distance of two agents for the smoker case.
            Cf. Schleussner et al. (2016), p. 8.
            
            Parameters
            ----------
            agent_i: Individual in the contact network
            agent_j: Individual in the contact network

            Returns
            -------
            Absolute value of difference of behavior variable of both agents, which is symmetric. 
            """
            return np.abs(agent_i.behavior - agent_j.behavior)


        @staticmethod
        def __social_influence(agent_list, interaction_network):
            """
            Updates behavior of all agent depending on agent's disposition and behavior of interacting agents.
            Only for the fully coupled case.
            
            Parameters
            ----------
            agent_list: list of Individual in contact network
            interaction_network: np.array[N,N] of dtype int comprising all interactions taking place during current time step
            """

            # TODO: LOOK AT THE FOLLOWING PARAMETER
            # Parameter controlling the equilibrium stochastic noise.
            C = 0.1
            # Create array of agent characteristics
            agent_behavior = np.zeros((len(agent_list),1),dtype="int8")
            # Create alike array for new, updated agent characteristics
            agent_behavior_update = agent_behavior.copy()

            # Get behavior of all agents of last time step
            for i in range(len(agent_list)):
                agent_behavior[i] = agent_list[i].behavior

            # Perform social influence for all agents in the contact network
            for agent in range(len(agent_list)):
                number_of_interactions = np.sum(interaction_network[agent,:])

                # Only change agent's behavior if interaction takes place
                if number_of_interactions != 0:

                    # create random number for potential behavior change
                    random_number = np.random.rand()
                    # if agent is non-smoker
                    if agent_list[agent].behavior == 0:
                        # Calculate probability of behavior change
                        change_probability = C * agent_list[agent].disposition\
                                             * np.sum(interaction_network[agent,:]* agent_behavior / number_of_interactions)
                        # Change behavior
                        agent_behavior_update[agent] = (random_number <= change_probability).astype("int8")
                    # if agent is smoker
                    else:
                        # calculate probability of behavioral change
                        change_probability = C * (1 - agent_list[agent].disposition)\
                                             * (1 - np.sum(interaction_network[agent,:] * agent_behavior / number_of_interactions))
                        # Change behavior
                        agent_behavior_update[agent] = 1 - (random_number <= change_probability).astype("int8")

                # If there are no interactions leave behavior unchanged
                else:
                    agent_behavior_update[agent] = agent_behavior[agent]
            # Write new agent behaviors from array to Individuals in contact network
            for i in range(len(agent_list)):
                agent_list[i].behavior = agent_behavior_update[i]



    def __init__(self,
                 *,
                 # TODO: Do I need the degree preference in CULTURE? Isn't that a property of the agent?
                 # TODO: Two things to consider: 1. The degree preference does not change during the simulation,  hence it can easily be stored in an array which is an attribute of culture. 2. For the sake of clarity and to uphold the idea of the framework, the degree preference can be extracted from each agent at every step. QUESTION: Is this too slow?
                 degree_preference=None,
                 # For a given agent, this function executes the behavioral change
                 # Here it is possible to implement various
                 social_influence,
                 # TODO: REALLY CLEVER TO USE ONE HUGE DICTIONARY FOR MODEL PARAMETERS?
                 model_parameters,
                 social_distance_function = None,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)  # must be the first line

        # exception
        #if not callable()

        # TODO: insert assert statements


        # set internal variables and functions

        self.n_individual = model_parameters.n_individual
        self.mean_degree_pref = model_parameters.mean_degree_pref
        self.std_degree_pref = model_parameters.std_degree_pref
        self.p_rew = model_parameters.p_rew
        self.char_weight = model_parameters.char_weight
        self.interaction_offset = model_parameters.interaction_offset
        self.p_ai = model_parameters.p_ai


        # provide standard social distance function
        if social_distance_function is None:
            self.social_distance_function = self.__social_distance_smoker_function
        else:
            self.social_distance = social_distance_function

        if social_influence is None:
            self.social_influence = self.__social_influence
        else:
            self.social_influence = social_influence


        # set additional variables

        # create nodes list from friendship network
        self.__nodes = self.friendship_network.nodes()

        # initialise background proximity network
        proximity_network = igraph.GraphBase.Lattice([self.n_individual],
                                                     nei=int(float(self.mean_degree_pref) / 2.0),
                                                     directed=False, mutual=True, circular=True)
        proximity_network.rewire(int(self.p_rew * self.n_individual * self.mean_degree_pref))
        small_world_distance_matrix = np.asarray(proximity_network.shortest_paths())

        # Generate random noise
        random_prox_noise = np.random.random((self.n_individual, self.n_individual))
        random_prox_noise = (random_prox_noise + random_prox_noise.transpose()) * .5

        # Derive the background proximity matrix with added noise to generate a continuum
        self.__background_proximity = (1 - .1 * (small_world_distance_matrix - 1) - 0.1 *
                                  random_prox_noise)

        # Introduce a proximity offset
        # For high degrees of separation there is no proximity difference anymore
        self.__background_proximity[np.where(self.__background_proximity <= 0.2)] = 0.2

        # make sure there are no self-loops
        for k in range(self.__background_proximity.shape[0]):
            self.__background_proximity[k, k] = 0

        pass


    def some_configure_method(self, other_argument):
        """
        This method should provide some configuration interface for the run file, although this might not be necessary because of the constructor
        
        :param other_argument: 
        :return: 
        """
        pass
    # process-related methods:


    # IS THERE A FASTER WAY FOR THIS?
    def get_proximity_matrix(self):
        '''
        
        Parameters:
        -----------
            
        Returns:
        --------
            
        '''

        distances = np.zeros(self.n_individual, self.n_individual)

        for i in range(self.n_individual):
            for j in range(self.n_individual):
                distances[i][j] = self.char_weight[0] \
                                  * np.abs(np.abs(self.social_distance_function(self.__nodes[i],self.__nodes[j])) - 1)

        return distances + self.char_weight[1] * self.__background_proximity



    def generate_interaction_network(self):
        """
        
        Returns
        -------

        """

        # Create a numpy array containing all path lengths from the friendship network
        # Convert networkx graph to igraph graph via edge list (fastest way)
        transformed_network = igraph.Graph(n=len(self.n_individual),
                                           edges=list(zip(*list(zip(*nx.to_edgelist(self.friendship_network)))[:2])))
        #  Perform Dijkstra algorithm that is much faster in igraph
        distance_metric_matrix = np.array(transformed_network.shortest_paths(), dtype=float)

        interaction_probability_matrix = (self.p_ai - self.interaction_offset) * \
                  np.exp(-(distance_metric_matrix - 1) / 2.)

        # Find longest path
        distmax = distance_metric_matrix[np.isfinite(distance_metric_matrix)].max()

        # TODO: Proper inline comments...
        # Create histogram using shortest and longest path
        histo_bins = np.arange(1, distmax)

        histo_range = [histo_bins.min(), histo_bins.max()]
        distribution = np.histogram(distance_metric_matrix.flatten(), histo_bins, range=histo_range)

        for i in distribution[1][:-1]:
            interaction_probability_matrix[distance_metric_matrix == i] *= (float(distribution[0][0]) / distribution[0][i - 1])

        interaction_probability_matrix += self.interaction_offset

        # Draw uniformly distributed random numbers from the interval [9,1]
        random_numbers = np.random.rand(self.n_individual,self.n_individual)
        # Symmetrize
        random_numbers = (random_numbers + random_numbers.transpose()) / 2.

        # Return adjacency matrix of interaction network
        return (random_numbers <= interaction_probability_matrix).astype("int8")


    # TODO: FUNCTION NEEDED?
    def perform_social_influence(self):
        """
        Changes behavior of one agent behavior depending on Culture's social_influence function, the agent's disposition, and
        (potentially, given the function) the behavior of agent's neighbors.
        
        Returns
        -------
        

        """

 #

        pass


    def update_contact_network(self):

        proximity_matrix = self.get_proximity_matrix()
        old_contact_network = nx.adjacency_matrix(self.friendship_network)



        pass

    def compute_conditional_behavior_probability(self):
        pass

    # MAYBE THESE MEASURES SHOULD BE VARIABLES AND BE COMPUTED AFTER EAcH STEP...
    def compute_centrality_measures(self):
        pass
    #return something


    def step_time(self, t):
        """
        Increase simulation time by one step.
        
        Parameters
        ----------
        t

        Returns
        -------
        New simulation time that is increased by one step.

        """
        return t + 1


    def one_step(self, t):
        """
        
        Parameters
        ----------
        t

        Returns
        -------

        """
        pass

    processes = []  # TODO: instantiate and list process objects here
