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
    def __kolmogorov_smirnov_test(self, current_distribution, target_distribution, distribution_function):
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
                cdf[i] = scipy.integ.quad(lambda x: distribution_function(x),
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
            new_distribution = (current_distribution + tr_noise_coeff * random_sign *
                              random_noise_increase * distr_dev)
            # check for boundaries, keep the old values where the new values exceed boundaries
            new_distribution[new_distribution > 1] = current_distribution[new_distribution > 1]
            new_distribution[new_distribution < 0] = current_distribution[new_distribution < 0]

            # Kolmogorov-Smirnov test
            kolm_smir_step = scipy.stats.kstest(new_distribution, integrate_cdf)[0]
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
        # If transition works, return new distribution
        return new_distribution


    def __calculate_transition_array(self, distribution_function, parameter_array):

        # produce distribution function
        # create transition array for agent characteristics
        # produce first distribution using rejection sampling
        #
        # for i in parameter_range:
        #   create distribution function from parameter value
        #   create new distribution using rejection sampling
        #   array.append(self.__kolmogorov_smirnov_test(current_distribution, new_distribution, distribution_function))
        # return transition array
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
        agent_list: list of Individuals in contact network
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
                 # For a given agent, this function executes the behavioral change
                 # Here it is possible to implement various
                 social_influence = None,
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

        self.n_individual = model_parameters['n_individuals']
        self.mean_degree_pref = model_parameters['mean_degree_pref']
        self.std_degree_pref = model_parameters['std_degree_pref']
        self.p_rew = model_parameters['p_rew']
        self.char_weight = model_parameters['char_weight']
        self.interaction_offset = model_parameters['interaction_offset']
        self.p_ai = model_parameters['p_ai']


        # provide standard social distance function
        if social_distance_function is None:
            self.social_distance_function = self.__social_distance_smoker_function
        else:
            self.social_distance = social_distance_function

        # provide standard social influence function
        if social_influence is None:
            self.perform_social_influence = self.__social_influence
        else:
            self.perform_social_influence = social_influence


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



    # TODO: Until I have understood Hooks, it's probably best to put all configurations into the following method,
    # TODO: which is called before a run.
    # TODO: CHECK if it is clever to pass te erdosrenyify function to this method. It's nicer than changing the contact
    # TODO: network from the run file.
    # TODO: Should the erdosrenyify method check if the degree preference is satisfied?

    def configure(self, generate_initial_contact_network):
        """
        This method should provide some configuration interface for the run file, although this might not be necessary because of the constructor
        
        :param other_argument: 
        :return: 
        """

        # create nodes list from friendship network
        self.__nodes = self.friendship_network.nodes()

        self.degree_preference = []
        for i in range(self.n_individual):
            self.degree_preference[i] = self.__nodes[i].degree_preference

        generate_initial_contact_network(self.friendship_network)

        pass
    # process-related methods:


    # TODO: IS THERE A FASTER WAY FOR THIS?
    def get_proximity_matrix(self):
        """
        Generate proximity matrix using background proximity and current agent behavior.
        Returns
        -------
        proximity matrix: ndarray[N,N]
        """

        distances = np.zeros(self.n_individual, self.n_individual)

        for i in range(self.n_individual):
            for j in range(self.n_individual):
                distances[i][j] = self.char_weight[0] \
                                  * np.abs(np.abs(self.social_distance_function(self.__nodes[i],self.__nodes[j])) - 1)

        return distances + self.char_weight[1] * self.__background_proximity



    def generate_interaction_network(self):
        """
        Generate interaction network using current distances in friendship network.
        
        Returns
        -------
        interaction network: ndarray[N,N]

        """

        # Create a numpy array containing all path lengths from the friendship network
        # Convert networkx graph to igraph graph via edge list (fastest way)
        transformed_network = igraph.Graph(n=len(self.n_individual),
                                           edges=list(zip(*list(zip(*nx.to_edgelist(self.friendship_network)))[:2])))
        #  Perform Dijkstra algorithm that is much faster in igraph
        distance_metric_matrix = np.array(transformed_network.shortest_paths(), dtype=float)

        # Create interaction probability matrix using formula from Schleussner et al. with an exponential decay
        # depending on distance in the network
        interaction_probability_matrix = (self.p_ai - self.interaction_offset) * \
                  np.exp(-(distance_metric_matrix - 1) / 2.)

        # Find longest path
        distmax = distance_metric_matrix[np.isfinite(distance_metric_matrix)].max()

        # Create histogram using shortest and longest path
        histo_bins = np.arange(1, distmax)

        histo_range = [histo_bins.min(), histo_bins.max()]
        distribution = np.histogram(distance_metric_matrix.flatten(), histo_bins, range=histo_range)

        # Apply normalization factor for all path lengths in the network
        for i in distribution[1][:-1]:
            interaction_probability_matrix[distance_metric_matrix == i] *= (float(distribution[0][0]) / distribution[0][i - 1])

        # Apply offset
        interaction_probability_matrix += self.interaction_offset

        # Draw uniformly distributed random numbers from the interval [9,1]
        random_numbers = np.random.rand(self.n_individual,self.n_individual)

        # Make array of random numbers symmetric, because interaction probability between i and j is equal to
        # interaction probability of j and i
        random_numbers = (random_numbers + random_numbers.transpose()) / 2.

        # Return adjacency matrix of interaction network
        self.interaction_network = int(random_numbers <= interaction_probability_matrix)



    def update_contact_network(self, interaction_network, proximity_matrix):

        #proximity_matrix = self.get_proximity_matrix()
        old_contact_network_adj = nx.to_numpy_matrix(self.friendship_network)

        potential_contact_indices = []

        new_contact_network_adj = np.zeros((self.n_individual,self.n_individual))

        for i in range(self.n_individual):
            # indices of friends in contact network
            contact_indices = np.where(old_contact_network_adj[i:] == 1)[1]

            # indices in interaction network
            interaction_indices = np.where(interaction_network[i,:] == 1)[1]

            # Combine both lists and discard repeated entries
            indices = np.unique(np.append(contact_indices, interaction_indices))

            # Get proximity values for given index list
            similarities = proximity_matrix[i, indices]

            # Sort unique list of contacts by social proximity of these contacts
            # Cut list at degree preference of agent
            sorted_indices = indices[similarities.argsort()][-self.degree_preference[i]:]

            # Append sorted indices array to potential contact indices array
            potential_contact_indices.append(sorted_indices)


        # check for bidirectionality
        for i in range(self.n_individual):
            filtered_indices = []

            for j in potential_contact_indices[i]:
                if i in potential_contact_indices[j]:
                    filtered_indices.append(j)
            new_contact_network_adj[i, filtered_indices] = 1

        self.friendship_network = nx.from_numpy_matrix(new_contact_network_adj)

    # def compute_conditional_behavior_probability(self, max_deg_sep):
    #
    #     # Create a numpy array containing all path lengths from the friendship network
    #     # Convert networkx graph to igraph graph via edge list (fastest way)
    #     transformed_network = igraph.Graph(n=len(self.n_individual),
    #                                        edges=list(zip(*list(zip(*nx.to_edgelist(self.friendship_network)))[:2])))
    #     #  Perform Dijkstra algorithm that is much faster in igraph
    #     distance_metric_matrix = np.array(transformed_network.shortest_paths(), dtype=float)
    #
    #     cond_beh_prob = np.zeros(5)
    #     smokers = self.friendship_network[]
    #     for i in range(self.n_individual):
    #         if self.__nodes[i].behavior == 1:
    #             smokers.append(i)
    #
    #     for i in range(max_deg_sep):
    #         deg_sep = i + 1
    #         smoking_dep = []
    #         for
    #     # TODO: CHANGE THE FOLLOWING FUNCTION
    #     def calc_cond_prob(smokers, nw_full, deg_sep_max, N):
    #         """
    #         Add docstring!
    #         """
    #         rcp = np.zeros(5)
    #         for i in range(deg_sep_max):
    #             deg_sep = i + 1
    #             smoking_dep = []
    #             for node in smokers:
    #                 distance_matrix = nw_full.path_lengths()
    #                 contact_one = np.where(distance_matrix[node, :] == deg_sep)
    #                 if contact_one[0].size > 0:
    #                     smoking_dep.append(
    #                         np.sum(nw_full.node_attribute('smoker')[contact_one]) /
    #                         float(contact_one[0].size) / (float(len(smokers)) / N) - 1)
    #             rcp[i] = np.mean(smoking_dep)
    #         return rcp
    #     pass

    # MAYBE THESE MEASURES SHOULD BE VARIABLES AND BE COMPUTED AFTER EAcH STEP...
    # TODO: Think about status of this method...
    def compute_centrality_measures_smokers(self):
        # get agent characteristics
        agent_behavior = np.zeros((len(self.n_individual),1),dtype="int8")
        for i in range(self.n_individual):
            agent_behavior[i] = self.__nodes[i].behavior
        # TODO: CHECK THAT!
        smokers = np.where(agent_behavior == 1)[1]
        non_smokers = np.where(agent_behavior == 0)[1]

        transformed_network = igraph.Graph(n=len(self.n_individual),
                                           edges=list(zip(*list(zip(*nx.to_edgelist(self.friendship_network)))[:2])))
        self.eigenvector_centrality["smokers"] = np.mean(
            np.asarray(transformed_network.graph.evcent(scale=False))[smokers])
        self.eigenvector_centrality["non-smokers"] = np.mean(
            np.asarray(transformed_network.graph.evcent(scale=False))[non_smokers])


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

        # generate_interaction_network
        interaction_network = self.generate_interaction_network()
        # perform social influence
        self.perform_social_influence(self.__nodes, interaction_network)
        # calculate proximity matrix
        proximity_matrix = self.get_proximity_matrix()
        # update contact network
        self.update_contact_network(interaction_network, proximity_matrix)

        # TODO: MEASURE OBSERVABLES
        # Optionally apply external forcing
        # self.apply_forcing()

        pass

    processes = [
        Step()
    ]  # TODO: instantiate and list process objects here
