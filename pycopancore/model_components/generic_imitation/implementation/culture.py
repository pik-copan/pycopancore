"""Culture process taxon mixing class template.
"""

"""
TODO:
- override attr/fct names end in _key for modularisation
- dose-response
- performance --> learning
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

def get_entry(spec, my_trait, other_trait):
    """extract value for trait pair from specification, 
    which, if it is a dict, can either contain the pair 
    or the pair with one or both entries replaced by '*', or neither."""
    if hasattr(spec, '__call__'):
        return spec(own_trait=my_trait, other_trait=other_trait)
    elif isinstance(spec, dicttype):
        if (my_trait, other_trait) in spec.keys(): return spec[(my_trait, other_trait)]
        if (my_trait, '*') in spec.keys(): return spec[(my_trait, '*')]
        if ('*', other_trait) in spec.keys(): return spec[('*', other_trait)]
        if ('*', '*') in spec.keys(): return spec[('*', '*')]
        return None
    else:
        return spec

def get_entry_or_return_value(spec, me, my_trait, other_trait):
    """extract value for trait pair from specification, 
    which, if it is a dict, can either contain the pair 
    or the pair with one or both entries replaced by '*', or neither."""
    if hasattr(spec, '__call__'):
        return spec(me, own_trait=my_trait, other_trait=other_trait)
    elif isinstance(spec, dicttype):
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
            # get all entities of the correct type that are governed by this culture:
            entities = [e for e in entity_type.instances if e.culture == self]

            # draw a batch of entities:

            p_in_batch = get_spec(self.imi_p_in_batch, key)
            batch_n = get_spec(self.imi_batch_n, key)
            if p_in_batch is not None:
                assert batch_n is None, "You cannot specify both imi_p_in_batch and imi_batch_n for "+str(key)
                # include each entity with probability p_in_batch or with its own imi_p_in_batch_<key>:
                pairs1 = [(e, getattr(e, 'imi_p_in_batch_'+key) if hasattr(e, 'imi_p_in_batch_'+key) 
                              else p_in_batch) for e in entities]
                pairs2 = [(e, p(e) if hasattr(p,'__call__') else p) for e,p in pairs1]
                batch = [e for e,p in pairs2 if p == 1 or (p > 0 and p > uniform())]
            elif batch_n is not None:
                # draw exactly batch_n many entities (or all, if there are fewer):
                batch = [] if batch_n == 0 else entities if len(entities) <= batch_n else choice(entities, size=batch_n, replace=False)
            else:
                raise Exception("Please specify either imi_p_in_batch or imi_batch_n for "+str(key))

            # most of the below code is only to make sure that 
            # at each time point and for each entity, source trait and target trait,
            # the correct imitation parameters are used.

            itype = get_spec(self.imi_type, key)
            network = get_spec(self.imi_network, key).get_value(self)  # since imi_networks specifies a Variable holding a network for each culture!
            default_p_imitate_spec = get_spec(self.imi_p_imitate, key)  # this might be a single value or a dict, see below!

            assert itype in ['simple', 'complex'], "Unknown imitation type "+str(itype)

            # determine direction if network is directed:
            if isinstance(network, DiGraph):
                direction = get_spec(self.imi_spreading_direction, key)
                assert direction is not None, "since network is directed, please specify imi_spreading_direction"
                nb_getter = network.predecessors if direction=='forward' else network.successors
            else:
                nb_getter = network.neighbors

            # determine which parameters depend on source and target trait:

            if isinstance(default_p_imitate_spec, dicttype):
                # imitation probabilities may depend on source and target
                p_imitate_keys = default_p_imitate_spec.keys()
                default_p_imitate_depends_on_source = any([source != '*' for (source, target) in p_imitate_keys])
                default_p_imitate_depends_on_target = any([target != '*' for (source, target) in p_imitate_keys])
                if not (default_p_imitate_depends_on_source or default_p_imitate_depends_on_target):
                    default_p_imitate = get_entry(default_p_imitate_spec, None, None)
                else:
                    default_p_imitate = None
            else:
                default_p_imitate_depends_on_source = default_p_imitate_depends_on_target = False
                default_p_imitate = default_p_imitate_spec

            if itype=='complex':
                default_n_neighbors_drawn = get_spec(self.imi_n_neighbors_drawn, key)
                default_p_neighbor_drawn = get_spec(self.imi_p_neighbor_drawn, key)
                default_abs_threshold_spec = get_spec(self.imi_abs_threshold, key)
                default_rel_threshold_spec = get_spec(self.imi_rel_threshold, key)

                if isinstance(default_abs_threshold_spec, dicttype):
                    default_abs_threshold_keys = default_abs_threshold_spec.keys()
                    default_abs_threshold_depends_on_source = any([source != '*' for (source, target) in default_abs_threshold_keys])
                    default_abs_threshold_depends_on_target = any([target != '*' for (source, target) in default_abs_threshold_keys])
                    if not (default_abs_threshold_depends_on_source or default_abs_threshold_depends_on_target):
                        default_abs_threshold = get_entry(default_abs_threshold_spec, None, None)
                    else:
                        default_abs_threshold = None
                else:
                    default_abs_threshold_depends_on_source = default_abs_threshold_depends_on_target = False
                    default_abs_threshold = default_abs_threshold_spec

                if isinstance(default_rel_threshold_spec, dicttype):
                    default_rel_threshold_keys = default_rel_threshold_spec.keys()
                    default_rel_threshold_depends_on_source = any([source != '*' for (source, target) in default_rel_threshold_keys])
                    default_rel_threshold_depends_on_target = any([target != '*' for (source, target) in default_rel_threshold_keys])
                    if not (default_rel_threshold_depends_on_source or default_rel_threshold_depends_on_target):
                        default_rel_threshold = get_entry(default_rel_threshold_spec, None, None)
                    else:
                        default_rel_threshold = None
                else:
                    default_rel_threshold_depends_on_source = default_rel_threshold_depends_on_target = False
                    default_rel_threshold = default_rel_threshold_spec

            # MAIN LOOP: process each batch member:
                
            for me in batch:

                # get all neighbors of me:
                neighbors = list(nb_getter(me))
                n_neighbors = len(neighbors)
                if n_neighbors == 0: 
                    continue  # no other to imitate

                # possibly override default_p_imitate by entity's own p_imitate_<key>:                
                if hasattr(me, 'imi_p_imitate_'+key):
                    actual_p_imitate_spec = getattr(e, 'imi_p_imitate_'+key)
                    if hasattr(actual_p_imitate_spec, '__call__'):
                        actual_p_imitate_depends_on_source = actual_p_imitate_depends_on_target = True
                        actual_p_imitate = None
                    else:
                        actual_p_imitate_depends_on_source = actual_p_imitate_depends_on_target = False
                        actual_p_imitate = actual_p_imitate_spec
                else:
                    actual_p_imitate_spec = default_p_imitate_spec
                    actual_p_imitate_depends_on_source = default_p_imitate_depends_on_source
                    actual_p_imitate_depends_on_target = default_p_imitate_depends_on_target
                    actual_p_imitate = default_p_imitate

                # if any of the actual probabilities depend on source trait, extract it:
                if actual_p_imitate_depends_on_source:
                    my_trait = tuple(var.get_value(me) for var in variables) 
                else:
                    my_trait = None             
                # already extract parameters that depend on source but not on target trait:
                if actual_p_imitate_depends_on_source and not actual_p_imitate_depends_on_target:
                    actual_p_imitate = get_entry_or_return_value(actual_p_imitate_spec, me, my_trait, None)
                    if actual_p_imitate == 0:
                        continue  # won't imitate
                    
                if itype=='complex':
                    
                    # possibly override other parameters by entity's own values:
                                        
                    if hasattr(me, 'imi_n_neighbors_drawn_'+key):
                        actual_n_neighbors_drawn = getattr(e, 'imi_n_neighbors_drawn_'+key)
                        if hasattr(actual_n_neighbors_drawn, '__call__'):
                            actual_n_neighbors_drawn = actual_n_neighbors_drawn(me)
                    else:
                        actual_n_neighbors_drawn = default_n_neighbors_drawn 
                    if actual_n_neighbors_drawn == 0:
                        continue  # no-one to imitate
                    elif actual_n_neighbors_drawn > n_neighbors:
                        actual_n_neighbors_drawn = n_neighbors

                    if hasattr(me, 'imi_p_neighbor_drawn_'+key):
                        actual_p_neighbor_drawn = getattr(e, 'imi_p_neighbor_drawn_'+key)
                        actual_p_neighbor_drawn_depends_on_neighbor = hasattr(actual_p_neighbor_drawn, '__call__')
                    else:
                        actual_p_neighbor_drawn = default_p_neighbor_drawn 
                        actual_p_neighbor_drawn_depends_on_neighbor = False
                    if actual_p_neighbor_drawn == 0:
                        continue  # no-one to imitate
   
                    if hasattr(me, 'imi_abs_threshold_'+key):
                        actual_abs_threshold_spec = getattr(e, 'imi_abs_threshold_'+key)
                        if hasattr(actual_abs_threshold_spec, '__call__'):
                            actual_abs_threshold_depends_on_source = actual_abs_threshold_depends_on_target = True
                            actual_abs_threshold = None
                        else:
                            actual_abs_threshold_depends_on_source = actual_abs_threshold_depends_on_target = False
                            actual_abs_threshold = actual_abs_threshold_spec
                    else:
                        actual_abs_threshold_spec = default_abs_threshold_spec
                        actual_abs_threshold_depends_on_source = default_abs_threshold_depends_on_source
                        actual_abs_threshold_depends_on_target = default_abs_threshold_depends_on_target
                        actual_abs_threshold = default_abs_threshold
                    try:
                        if actual_abs_threshold > actual_n_neighbors_drawn:
                            continue  # won't imitate
                    except: pass

                    if hasattr(me, 'imi_rel_threshold_'+key):
                        actual_rel_threshold_spec = getattr(e, 'imi_rel_threshold_'+key)
                        if hasattr(actual_rel_threshold_spec, '__call__'):
                            actual_rel_threshold_depends_on_source = actual_rel_threshold_depends_on_target = True
                            actual_rel_threshold = None
                        else:
                            actual_rel_threshold_depends_on_source = actual_rel_threshold_depends_on_target = False
                            actual_rel_threshold = actual_rel_threshold_spec
                    else:
                        actual_rel_threshold_spec = default_rel_threshold_spec
                        actual_rel_threshold_depends_on_source = default_rel_threshold_depends_on_source
                        actual_rel_threshold_depends_on_target = default_rel_threshold_depends_on_target
                        actual_rel_threshold = default_rel_threshold
                    try:
                        if actual_rel_threshold > 1:
                            continue  # won't imitate
                    except: pass
                    
                # finally perform the actual imitation:
                
                if itype=='simple':
                    
                    # draw one other:
                    other = choice(neighbors)
                    
                    # check whether to imitate them:
                    if actual_p_imitate_depends_on_target: 
                        other_trait = tuple(var.get_value(other) for var in variables)
                        actual_p_imitate = get_entry_or_return_value(actual_p_imitate_spec, me, my_trait, other_trait)
                        if other_trait == my_trait or actual_p_imitate == 0 or (actual_p_imitate < 1 and actual_p_imitate < uniform()):
                            continue # don't imitate
                        # else imitate, see below
                    else:
                        if actual_p_imitate == 0 or (actual_p_imitate < 1 and actual_p_imitate < uniform()):
                            continue # don't imitate
                        # else imitate, see below
                        other_trait = tuple(var.get_value(other) for var in variables)
                    
                else: # 'complex':
                    
                    # if any of the actual parameters depend on source trait, extract it and them if not done so:
                    if my_trait is None and (actual_abs_threshold_depends_on_source or actual_rel_threshold_depends_on_source):
                        my_trait = tuple(var.get_value(me) for var in variables) 
                    if actual_abs_threshold_depends_on_source and not actual_abs_threshold_depends_on_target:
                        actual_abs_threshold = get_entry_or_return_value(actual_abs_threshold_spec, me, my_trait, None)
                    if actual_rel_threshold_depends_on_source and not actual_rel_threshold_depends_on_target:
                        actual_rel_threshold = get_entry_or_return_value(actual_rel_threshold_spec, me, my_trait, None)
    
                    # draw some others:
                    if actual_p_neighbor_drawn is not None:
                        assert actual_n_neighbors_drawn is None, "You cannot specify both imi_p_neighbor_drawn and imi_n_neighbors_drawn for "+str(key)
                        # include each neighbor with probability p_neighbor_drawn:
                        others = [e for e in neighbors 
                                  if uniform() < (actual_p_neighbor_drawn(me, neighbor=e) 
                                                  if actual_p_neighbor_drawn_depends_on_neighbor 
                                                  else actual_p_neighbor_drawn)]
                    elif actual_n_neighbors_drawn is not None:
                        # draw exactly n_neighbors_drawn many neighbors (or all, if there are fewer):
                        others = neighbors if len(neighbors) <= actual_n_neighbors_drawn \
                                 else choice(neighbors, size=actual_n_neighbors_drawn, replace=False)
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
                        if actual_abs_threshold_depends_on_target: 
                            actual_abs_threshold = get_entry_or_return_value(actual_abs_threshold_spec, me, my_trait, other_trait)
                        if actual_rel_threshold_depends_on_target: 
                            actual_rel_threshold = get_entry_or_return_value(actual_rel_threshold_spec, me, my_trait, other_trait)
                        assert actual_abs_threshold is None or actual_rel_threshold is None, "You cannot specify both imi_abs_threshold and imi_rel_threshold for "+str(key)
                        if ((actual_abs_threshold is not None) and freq >= actual_abs_threshold) \
                            or ((actual_rel_threshold is not None) and freq >= actual_rel_threshold * n_others):
                                # me potentially imitates this trait, so register it;
                                if actual_p_imitate_depends_on_target: 
                                    actual_p_imitate = get_entry_or_return_value(actual_p_imitate_spec, me, my_trait, other_trait) or 0
                                if actual_p_imitate > 0:
                                    targets.append(other_trait)
                                    ps.append(actual_p_imitate)
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
        rate_list = [get_spec(self.imi_rate, key) for key in self.imi_traits.keys()]
        return rate_list, sum(rate_list)
        