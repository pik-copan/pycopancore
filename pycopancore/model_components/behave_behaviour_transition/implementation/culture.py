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

    # NEEDED?
    __background_proximity = None
    __interaction_network = None

    def __kolmogorov_smirnov_test(self, current_distribution, desired_distribution):
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

        #  Define helper function
        def integrate_cdf(input_array):
            cdf = np.zeros(input_array.shape[0])
            for i in range(input_array.shape[0]):
                cdf[i] = integ.quad(lambda x: distribution_function(yb, x),
                                    0, input_array[i])[0]
            return cdf

        kolm_smir_step = 2

        # Kolm Smir target
        target = 0.1
        # noise scaling coeff
        tr_noise_coeff = 0.1

        # set counters
        k = 1
        n_inc = 0

        # derive the ideal distribution for given yb
        x = np.linspace(0, 1, 101)
        target_dist = distribution_function(yb, x)
        target_dist = target_dist * float(N) / (sum(target_dist))
        # get deviation
        hist_values_sample, hist_bins = np.histogram(
            disp_distr_t, bins=100, range=(0, 1))
        hist_values_sample = np.append(hist_values_sample, hist_values_sample[-1])
        hist_diff = hist_values_sample - target_dist
        # get the noise level for all N agents
        disp_distr_round = np.asarray(100 * disp_distr_t, dtype='int')
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
            disp_distr_tp1 = (disp_distr_t + tr_noise_coeff * random_sign *
                              random_noise_increase * distr_dev)
            # check for boundaries
            disp_distr_tp1[disp_distr_tp1 > 1] = disp_distr_t[disp_distr_tp1 > 1]
            disp_distr_tp1[disp_distr_tp1 < 0] = disp_distr_t[disp_distr_tp1 < 0]
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
                    return disp_distr_t
        return disp_distr_tp1

        pass


    def __init__(self,
                 *,
                 degree_preference=None,
                 # TODO: What does social influence do again?
                 social_influence,
                 # TODO: REALLY CLEVER TO USE ONE HUGE DICTIONARY FOR MODEL PARAMETERS?
                 model_parameters,
                 social_distance_function,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)  # must be the first line

        # exception
        #if not callable()

        # TODO: insert assert statements


        # set intern variables

        self.n_individual = model_parameters.n_individual
        self.mean_degree_pref = model_parameters.mean_degree_pref
        self.std_degree_pref = model_parameters.std_degree_pref
        self.p_rew = model_parameters.p_rew
        self.social_distance = social_distance_function
        self.char_weight = model_parameters.char_weight
        self.interaction_offset = model_parameters.interaction_offset
        self.p_ai = model_parameters.p_ai


        # create nodes list from friendship network
        self.__nodes = self.friendship_network.nodes()

        # initialise background proximity network
        proximity_network = igraph.GraphBase.Lattice([self.n_individual], nei=int(float(self.mean_degree_pref)/2.0),
                                                     directed=False, mutual=True, circular=True)
        proximity_network.rewire(int(self.p_rew * self.n_individual * self.mean_degree_pref))
        small_world_distance_matrix = np.asarray(proximity_network.shortest_paths())

        # Generate random noise
        random_prox_noise = np.random.random((self.n_individual,self.n_individual))
        random_prox_noise = (random_prox_noise + random_prox_noise.transpose()) * .5

        # Derive the background proximity matrix with added noise to generate a continuum
        __background_proximity = (1 - .1 * (small_world_distance_matrix-1) - 0.1 *
                             random_prox_noise)

        # Introduce a proximity offset
        # For high degrees of separation there is no proximity difference anymore
        __background_proximity[np.where(__background_proximity <= 0.2)] = 0.2

        # make sure there are no self-loops
        for k in range(__background_proximity.shape[0]):
            __background_proximity[k,k] = 0




        pass

    # process-related methods:


    #TODO: NEED TO IMPLEMENT GET CHARACTERISTICS FUNCTION IN INDIVIDUAL!
    #TODO: IS NUMPY ARRAY APPROPRIATE DATA TYPE?
    #TODO: Should this be a private method?
    def get_agents_characteristics(self):

        agent_characteristics = np.array([self.n_individual])

        for i in range(self.n_individual):
            #TODO: What is faster? Implementing via getter or direct access to attribute?
            agent_characteristics[i] = self.__nodes[i].behavior

        return agent_characteristics



    # IS THERE A FASTER WAY FOR THIS?
    # char_weight not yet defined
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
                distances[i][j] = self.char_weight[0] * np.abs(np.abs(
                    self.social_distance(self.__nodes[i],self.__nodes[j])) - 1)

        # char_weight not yet defined!
        return distances + self.char_weight[1] * self.__background_proximity



    def generate_interaction_network(self):

        # Create a numpy array containing all path lengths from the friendship network
        # Convert networkx graph to igraph graph via edge list (fastest way)
        transformed_network = igraph.Graph(n=len(self.n_individual),
                                           edges=list(zip(*list(zip(*nx.to_edgelist(self.friendship_network)))[:2])))
        #  Perform Dijkstra algorithm that is much faster in igraph
        distance_metric_matrix = np.array(transformed_network.shortest_paths(), dtype=float)

        #TODO: define p_ai and interaction_offset

        exp_dec = (self.p_ai - self.interaction_offset) * \
                  np.exp(-(distance_metric_matrix - 1) / 2.)

        # Find longest path
        distmax = distance_metric_matrix[np.isfinite(distance_metric_matrix)].max()

        # TODO: Proper inline comments...
        # Create histogram using shortest and longest path
        histo_bins = np.arange(1, distmax)

        histo_range = [histo_bins.min(), histo_bins.max()]
        distribution = np.histogram(distance_metric_matrix.flatten(), histo_bins, range=histo_range)

        for i in distribution[1][:-1]:
            exp_dec[distance_metric_matrix == i] *= (float(distribution[0][0]) / distribution[0][i - 1])

        exp_dec += self.interaction_offset

        return exp_dec


    def update_social_influence(self):
        pass

    def update_contact_network(self):
        pass

    def one_step(self):
        pass



    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
