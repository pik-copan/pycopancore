"""Culture process taxon mixing class template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from numpy import any, array, inf, sum
from numpy.random import exponential, uniform, choice
from networkx import DiGraph

from .... import Event
from ... import config
from .. import interface as I

dicttype = type({})

def get_spec(spec, key):
    """extract value for key from specification, 
    which can either be a dict with the given key, a dict with key '*', or
    a single value."""
    if isinstance(spec, dicttype):
        if key in spec.keys(): return spec[key]
        if '*' in spec.keys(): return spec['*']
        return None
    else:
        return spec

def get_spec_pair(spec, my_trait, other_trait):
    """extract value for trait pair from specification, 
    which, if it is a dict, can either contain the pair 
    or the pair with one or both entries replaced by '*', or neither."""
    if isinstance(spec, dicttype):
        if (my_trait, other_trait) in spec.keys(): return spec[(my_trait, other_trait)]
        if (my_trait, '*') in spec.keys(): return spec[(my_trait, '*')]
        if ('*', other_trait) in spec.keys(): return spec[('*', other_trait)]
        if ('*', '*') in spec.keys(): return spec[('*', '*')]
        return None
    else:
        return spec

class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # public method declared in interface:
        
    def trigger_imitation(self, key="*"):
        """(see interface)"""
        keys = self.imi_traits if key=="*" else [key]
        feasible_vars = [expr.target_variable for expr in config.generic_imitation['variables']]
        
        for key in keys:

            variables = self.imi_traits[key]
            assert isinstance(variables, tuple), "Each entry in imi_traits must be of the form str: tuple(variable,...,variable). Single Variables must be specified as singleton tuples with a comma: (variable,)"
            if len(variables) == 0: continue
            entity_type = variables[0].owning_class
            for var in variables:
                assert var.owning_class == entity_type, "All variables in a trait must belong to the same entity type"
                assert var in feasible_vars, "All variables in a trait must be listed in config.generic_imitation['variables']"
            entities = entity_type.instances

            # draw a batch of entities:

            p_in_batch = get_spec(self.imi_p_in_batch, key)
            batch_n = get_spec(self.imi_batch_n, key)
            if p_in_batch is not None:
                assert batch_n is None, "You cannot specify both imi_p_in_batch and imi_batch_n for "+str(key)
                # include each entity with probability p_in_batch:
                batch = [e for e in entities if uniform() < p_in_batch]
            elif batch_n is not None:
                # draw exactly batch_n many entities (or all, if there are fewer):
                batch = entities if len(entities) <= batch_n else choice(entities, size=batch_n, replace=False)
            else:
                raise Exception("Please specify either imi_p_in_batch or imi_batch_n for "+str(key))

            # now perform the actual imitation:

            itype = get_spec(self.imi_types, key)
            network = get_spec(self.imi_networks, key).get_value(self)  # since imi_networks specifies a Variable holding a network for each culture!
            p_imitate = get_spec(self.imi_p_imitate, key)

            assert itype in ['simple', 'threshold'], "Unknown imitation type "+str(itype)

            # determine direction if network is directed:
            if isinstance(network, DiGraph):
                direction = get_spec(self.imi_spreading_direction, key)
                assert direction is not None, "since network is directed, please specify imi_spreading_direction"
                nb_getter = network.predecessors if direction=='forward' else network.successors
            else:
                nb_getter = network.neighbors

            # determine which parameters depend on source and target trait:

            if isinstance(p_imitate, dicttype):
                # imitation probabilities may depend on source and target
                p_imitate_keys = p_imitate.keys()
                p_imitate_depends_on_source = any([source != '*' for (source, target) in p_imitate_keys])
                p_imitate_depends_on_target = any([target != '*' for (source, target) in p_imitate_keys])
                if not (p_imitate_depends_on_source or p_imitate_depends_on_target):
                    this_p_imitate = get_spec_pair(p_imitate, None, None)
            else:
                p_imitate_depends_on_source = p_imitate_depends_on_target = False
                this_p_imitate = p_imitate

            if itype=='threshold':
                n_neighbors_drawn = get_spec(self.imi_n_neighbors_drawn, key)
                p_neighbor_drawn = get_spec(self.imi_p_neighbor_drawn, key)
                abs_threshold = get_spec(self.imi_abs_threshold, key)
                rel_threshold = get_spec(self.imi_rel_threshold, key)

                if isinstance(abs_threshold, dicttype):
                    abs_threshold_keys = abs_threshold.keys()
                    abs_threshold_depends_on_source = any([source != '*' for (source, target) in abs_threshold_keys])
                    abs_threshold_depends_on_target = any([target != '*' for (source, target) in abs_threshold_keys])
                    if not (abs_threshold_depends_on_source or abs_threshold_depends_on_target):
                        this_abs_threshold = get_spec_pair(abs_threshold, None, None)
                else:
                    abs_threshold_depends_on_source = abs_threshold_depends_on_target = False
                    this_abs_threshold = abs_threshold

                if isinstance(rel_threshold, dicttype):
                    rel_threshold_keys = rel_threshold.keys()
                    rel_threshold_depends_on_source = any([source != '*' for (source, target) in rel_threshold_keys])
                    rel_threshold_depends_on_target = any([target != '*' for (source, target) in rel_threshold_keys])
                    if not (rel_threshold_depends_on_source or rel_threshold_depends_on_target):
                        this_rel_threshold = get_spec_pair(rel_threshold, None, None)
                else:
                    rel_threshold_depends_on_source = rel_threshold_depends_on_target = False
                    this_rel_threshold = rel_threshold

            # MAIN LOOP: process each batch member:
                
            for me in batch:
                
                # if any parameters depend on source trait, extract it:
                if p_imitate_depends_on_source:
                    my_trait = tuple(var.get_value(me) for var in variables) 
                else:
                    my_trait = None                 
                # already extract parameters that depend on source but not on target trait:
                if p_imitate_depends_on_source and not p_imitate_depends_on_target:
                    this_p_imitate = get_spec_pair(p_imitate, my_trait, None)
                    
                # get all neighbors of me:
                neighbors = list(nb_getter(me))
                if len(neighbors) == 0: continue  # no other to imitate

                # determine whether to imitate:
                    
                if itype=='simple':
                    
                    # draw one other:
                    other = choice(neighbors)
                    
                    # check whether to imitate them:
                    if p_imitate_depends_on_target: 
                        other_trait = tuple(var.get_value(other) for var in variables)
                        if other_trait == my_trait or uniform() > get_spec_pair(p_imitate, my_trait, other_trait):
                            continue # don't imitate
                        # else imitate, see below
                    else:
                        if uniform() > this_p_imitate:
                            continue # don't imitate
                        # else imitate, see below
                        other_trait = tuple(var.get_value(other) for var in variables)
                    
                else: # 'threshold':
                    
                    if my_trait is None and (abs_threshold_depends_on_source or rel_threshold_depends_on_source):
                        my_trait = tuple(var.get_value(me) for var in variables) 
                    if abs_threshold_depends_on_source and not abs_threshold_depends_on_target:
                        this_abs_threshold = get_spec_pair(abs_threshold, my_trait, None)
                    if rel_threshold_depends_on_source and not rel_threshold_depends_on_target:
                        this_rel_threshold = get_spec_pair(rel_threshold, my_trait, None)
    
                    # draw some others:
                    if p_neighbor_drawn is not None:
                        assert n_neighbors_drawn is None, "You cannot specify both imi_p_neighbor_drawn and imi_n_neighbors_drawn for "+str(key)
                        # include each neighbor with probability p_neighbor_drawn:
                        others = [e for e in neighbors if uniform() < p_neighbor_drawn]
                    elif n_neighbors_drawn is not None:
                        # draw exactly n_neighbors_drawn many neigbors (or all, if there are fewer):
                        others = neighbors if len(neighbors) <= n_neighbors_drawn else choice(neighbors, size=n_neighbors_drawn, replace=False)
                    else:
                        raise Exception("Please specify either imi_n_neighbors_drawn or imi_p_neighbor_drawn for "+str(key))
                    n_others = len(others)
                    # count frequencies of other traits:
                    freqs = {}
                    for trait in zip(*[var.get_values(others) for var in variables]):
                        freqs[trait] = freqs.get(trait, 0) + 1
                        
                    # assemble probability distribution:
                    targets = []
                    ps = []
                    for (other_trait, freq) in freqs.items():
                        if other_trait == my_trait: 
                            continue
                        if abs_threshold_depends_on_target: 
                            this_abs_threshold = get_spec_pair(abs_threshold, my_trait, other_trait)
                        if rel_threshold_depends_on_target: 
                            this_rel_threshold = get_spec_pair(rel_threshold, my_trait, other_trait)
                        if ((this_abs_threshold is not None) and freq >= this_abs_threshold) \
                            or ((this_rel_threshold is not None) and freq >= this_rel_threshold * n_others):
                                # me potentially imitates this trait, so register it;
                                targets.append(other_trait)
                                if p_imitate_depends_on_target: 
                                    this_p_imitate = get_spec_pair(p_imitate, my_trait, other_trait) or 0.0
                                ps.append(this_p_imitate)
                    # complete the probability distribution by adding my_trait with remaining probability:
                    p_switch = sum(ps)
                    assert p_switch <= 1, "Impossible combination of thresholds and imitation probabilities!"
                    if p_switch < 1:
                        targets.append(my_trait)
                        ps.append(1 - p_switch)
                    # finally draw the trait to imitate:
                    other_trait = targets[choice(len(targets), p=ps)]
                    if other_trait == my_trait: 
                        continue # no actual imitation after all
                    # else imitate, see below
                    
                # if we reached this point, me will imitate other_trait:
                for index, var in enumerate(variables):
                    var.set_value(me, other_trait[index])
                    
    # other process-related methods:

    def next_event_time(self, t):
        """Called by runner. Time of next imitation of some variable(s)"""
        rate_list, total_rate = self.get_rates()
        # draw and return next timepoint at which on such event happens after current time t:
        return (inf if total_rate == 0 else t + exponential(1. / total_rate))

    def perform_event(self, t):
        """Called by runner. Choose a (group of) variables and trigger a batch imitation"""
        rate_list, total_rate = self.get_rates()
        key = choice(list(self.imi_traits.keys()), p = array(rate_list) / total_rate)  
        print("      trait key:", key)       
        self.trigger_imitation(key)
        
    processes = [
                 Event("imitate some trait(s) on some network(s)",
                       config.generic_imitation['variables'],
                       ["time", next_event_time, perform_event])                 
                ]

    # auxiliary methods:
    
    def get_rates(self):
        """return the total rate of imitation events across all imitation variables"""
        rate_list = [get_spec(self.imi_rates, key) for key in self.imi_traits.keys()]
        return rate_list, sum(rate_list)
        