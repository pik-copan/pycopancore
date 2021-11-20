"""
=============================
A generic imitation component
=============================

*****************
Imitation process
*****************

The imitation process works as follows:

*   The subject of imitation are one or more "variable traits". 
    Each variable trait is either given by a single variable 
    -- represented by a single-entry tuple `(variable,)` -- 
    or by a combination of variables -- represented by a longer tuple
    `(variable, ..., variable)`. The variable traits are listed in the parameter
    :py:attr:`Culture.imi_traits <interface.Culture.imi_traits>` in the form of
    a dictionary `{key: tuple, ..., key: tuple}`. The keys in this dictionary
    are arbitrary strings and can be used in the other parameters as well 
    (see below).

*   For each such variable trait, batch imitation events happens at random 
    time points with the specified probability rate 
    (:py:attr:`imi_rate <interface.Culture.imi_rate>`). 
    This means that the time intervals between these events are 
    exponentially distributed with an average length of 1/*rate*.
  
*   When a batch imitation event happens, first a batch of entities of the 
    relevant type is drawn at random, either with a fixed batch size
    (:py:attr:`imi_batch_n <interface.Culture.imi_batch_n>`) 
    or using certain participation probabilities 
    (:py:attr:`imi_p_in_batch <interface.Culture.imi_p_in_batch>`).
  
*   Then, in a random order, each entity in the batch independently does the 
    following:

    *   It chooses one (if :py:attr:`imi_type <interface.Culture.imi_type>` 
        is ``'simple'``) or several (if :py:attr:`imi_type <interface.Culture.imi_type>` 
        is ``'complex'``) of its neighbors in some network (which is 
        specified in :py:attr:`imi_network <interface.Culture.imi_network>`).
        If the network is directed, this can be either a subset of predecessors
        or a subset of successors (this is set by 
        :py:attr:`imi_spreading_direction <interface.Culture.imi_spreading_direction>`). 
        In the 'complex' case, the set of chosen neighbors either has a fixed size 
        (:py:attr:`imi_n_neighbors_drawn <interface.Culture.imi_n_neighbors_drawn>`)
        or each neighbor has some probability to be in it
        (:py:attr:`imi_p_neighbor_drawn <interface.Culture.imi_p_neighbor_drawn>`).
        
    *   If 'simple', the chosen neighbor's trait (i.e., their combination of 
        the respective variable values) becomes the *candidate trait*. 
        If 'complex', the *candidate traits* are those that occur in
        at least a certain number
        (:py:attr:`imi_abs_threshold <interface.Culture.imi_abs_threshold>`)
        or a certain fraction 
        (:py:attr:`imi_rel_threshold <interface.Culture.imi_rel_threshold>`)
        of the chosen neighbors.
        If :py:attr:`imi_include_own_trait <interface.Culture.imi_include_own_trait>`
        is *True*, the entity's own trait is an additional candidate trait.
        
    *   Then one of these candidate traits is chosen as the *nominated trait*. 
        If there is only one candidate trait, that one is nominated.
        If there are several candidate traits, one of them is chosen randomly.
        By default, all candidate traits have the same probability in this.
        However, if the entity provides a method ``imi_evaluate_<key> (self, other)`` 
        (where ``<key>`` is the respective variable trait's key used in 
        :py:attr:`Culture.imi_traits <interface.Culture.imi_traits>`),
        then the selection probability of a candidate trait is based on the
        return value of this method averaged over all those chosen neighbors 
        that have the trait. If this average evaluation is *x*, the probability
        for the trait being nominated is proportional to exp(*x*/*delta*), 
        where *delta* is given by the parameter 
        :py:attr:`Culture.imi_delta <interface.Culture.imi_delta>`. 
        The smaller *delta*, the more likely the trait with the largest average
        evaluation will be nominated. The larger *delta*, the less influence
        have the evaluations on the nomination.   
    
    *   Finally, the entity imitates the nominated trait (i.e. adopts the 
        respective variable values) with a certain probability (given by
        :py:attr:`Culture.imi_p_imitate <interface.Culture.imi_p_imitate>`).
        By default, the variable values are copied exactly.
        However, if the entity provides a method 
        ``imi_imitate_<key> (self, other)``,
        then this method is called instead. This can be used to copy values
        only with some random error.
        
*   In this, all parameter values may be different for each variable trait.
    In addition, thresholds and imitation probabilities may depend on the entity's
    current trait and/or the candidate trait. To achieve this, the respective
    parameter variables have to provide a dict (or a dict of dicts) of values 
    keyed by the variable trait key and potentially by pairs of the
    form *(own trait, other trait)*, where both traits are given as
    tuples of the form *(value, ..., value)*.

*   Also, the parameter values given by the variables
    :py:attr:`imi_p_in_batch <interface.Culture.imi_p_in_batch>`,
    :py:attr:`imi_include_own_trait <interface.Culture.imi_include_own_trait>`,
    :py:attr:`imi_n_neighbors_drawn <interface.Culture.imi_n_neighbors_drawn>`,
    :py:attr:`imi_p_neighbor_drawn <interface.Culture.imi_p_neighbor_drawn>`,
    :py:attr:`imi_abs_threshold <interface.Culture.imi_abs_threshold>`,
    :py:attr:`imi_rel_threshold <interface.Culture.imi_rel_threshold>` and
    :py:attr:`imi_p_imitate <interface.Culture.imi_p_imitate>`
    in the `Culture` taxon may be overridden by the imitating entity by
    providing entity variables or methods named 
    ``imi_p_in_batch_<key>``, ..., ``imi_p_imitate_<key>``,
    where ``<key>`` is again the variable trait's key.
    See the individual parameter documentations for details.

*************
Special cases
*************

Simple contagion
================
One neighbor is drawn at random and their trait is imitated with certainty.
To achieve this, put ``imi_type = 'simple'``, ``imi_include_own_trait = False``,
and ``imi_p_imitate = 1.0``.

Simple social learning
======================
One neighbor is drawn at random and their trait is imitated with a probability
that depends on the difference between the neighbor's and the entity's value
of a certain variable in a sigmoidal way.
To achieve this, put ``imi_type = 'simple'``, ``imi_include_own_trait = True``,
``imi_p_imitate = 1.0``, choose some ``imi_delta`` larger than zero, 
and define the following method in the respective entity type::
    def imi_evaluate_<key> (self, other): return other.<variable>

'Meet two' complex contagion
============================
Two neighbors are drawn at random and if they agree in their trait, 
that trait is imitated with certainty.
To achieve this, put ``imi_type = 'complex'``,
``imi_n_neighbors_drawn = 2``, ``imi_abs_threshold = 2`` (or ``imi_rel_threshold = 1.0``), 
``imi_include_own_trait = False``, and ``imi_p_imitate = 1.0``.

'Take the best' social learning
===============================
The trait of the neighbor with the largest value in some variable 
(if larger than the entity's own value) is imitated with certainty.
To achieve this, put ``imi_type = 'complex'``, 
``imi_p_neighbor_drawn = 1.0``, ``imi_abs_threshold = 0`` (or ``imi_rel_threshold = 0.0``),
``imi_include_own_trait = True``, ``imi_p_imitate = 1.0``, ``imi_delta = 0.0``, 
and define the following method in the respective entity type::
    def imi_evaluate_<key> (self, other): return other.<variable>

Granovetter-style threshold-based activation
============================================
If at least a certain fraction *x* of neighbors are 'active', 
become 'active' with some probability *p*,
and never become 'inactive' again.
To achieve this, put ``imi_type = 'complex'``, 
``imi_p_neighbor_drawn = 1.0``, ``imi_rel_threshold = { (('inactive',), ('active',)): <x>, '*': inf }``
``imi_include_own_trait = False``, and ``imi_p_imitate = <p>``. 
In this, the entry ``'*': inf`` means that all other transitions except
from 'inactive' to 'active' require an infinite threshold and are thus impossible.
 
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# make sure model composer has named the variables to imitate before importing the component:
from .. import config
try:
    config.generic_imitation['variables']
except:
    config.generic_imitation = {'variables': []}
    print("WARNING (model component generic_imitation): Empty list of variables! Before importing generic_imitation in the model definition, you must import config from model_components and set config.generic_imitation['variables'].")

from . import interface
from . import interface as I

# export all implementation classes:
from .implementation import *

# export model component mixin class:
from .model import Model
