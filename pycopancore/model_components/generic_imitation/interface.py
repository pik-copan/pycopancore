"""model component Interface template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from typing import List, Dict, Union, Tuple, Any
from networkx import Graph, DiGraph

from ... import master_data_model as D
from ...data_model.master_data_model import CUL, I
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "generic imitation of traits on networks"
    """a unique name for the model component"""
    description = "For each of a list of variables, a certain fraction of entities of the variable's owning type looks at a certain number of fraction of their neighbors on a certain network and imitates their variable values with certain probabilities when certain thresholds are met. All these specifics are governed by parameters in Culture." 
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# process taxa:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # exogenous variables / parameters:
        
    imi_traits = Variable(
        "imitation traits",
        "Dict of key: trait. Each trait is a tuple of one or more Variables that shall be imitated together. Each occurring Variable must also be listed in the global variable generic_imitation_variables. All other imi_* parameters are allowed to be dictionaries keyed with the keys listed here, or with the key '*' for specifying values to be applied to all (other) entries occurring here.",
        datatype = Dict[str, Tuple[Variable]], 
        default={})

    imi_rates = Variable(
        "imitation rates",
        "(Dict of) rates at which a batch of entities imitates",
        datatype = Union[float, Dict[str, float]],
        unit=D.years**-1, lower_bound=0, default=0)
    # NOTE: imitation can also be triggered from other components by calling ...
            
    imi_p_in_batch = Variable(
        "probabilities of being in an imitation batch",
        "(Dict of) probabilities with which entities are selected to be in an imitation batch. Alternatively, imi_batch_n can be specified, but not both.",
        datatype = Union[float, Dict[str, float]],
        unit=D.unity, lower_bound=0, upper_bound=1, allow_none=True, default=None)
    
    imi_batch_n = Variable(
        "imitation batch sizes",
        "(Dict of) sizes of batches imitating at the same time. Alternatively, imi_p_in_batch can be specified, but not both.",
        datatype = Union[int, Dict[str, int]],
        unit=D.unity, quantum=1, lower_bound=0, allow_none=True, default=None)
        
    imi_types = Variable(
        "imitation types",
        "(Dict of) string(s) specifying the type(s) of imitation: 'simple' means entities draw one neighbor and imitate it with some probability. 'threshold' means entities draw several neighbors and imitate each observed value occurring above a certain threshold with some probability.",
        datatype = Union[str, Dict[str, str]],
        scale='nominal', levels=['simple', 'threshold'], default='simple')

    imi_networks = Variable(
        "imitation networks",
        "(Dict of) Variable object(s) containing the network(s) imitation is based on.",
        datatype = Union[Graph, DiGraph, Dict[str, Union[Graph, DiGraph]]])
        
    imi_spreading_direction = Variable(
        "imitation spreading direction",
        "(Dict of) 'forward' or 'backward'. Only applicable if network is directed. If 'forward', nodes imitate their predecessors, if 'backward', they imitate their successors in the directed network",
        datatype = Union[str, Dict[str, str]], allow_none=True, default=None)

    imi_p_imitate = Variable(
        "imitation probabilities",
        "(Dict of (dict of)) probability(ies) to actually imitate the candidate value (in the 'simple' case, the value of a randomly drawn neighbor, in the 'threshold' case, each value occurring in the drawn neighbors more often than the thresholds say). If dict of dict, inner dict keys must be of the form (source value, target value), where both source and target values might be '*' to indicate that this entry applies to all source or target values.",
        datatype = Union[float, Dict[str, float], Dict[str, Dict[Tuple[Any, Any], float]]],
        unit=D.unity, lower_bound=0, upper_bound=1, default=1)
        
    # only applicable to type='threshold':#
    
    imi_n_neighbors_drawn = Variable(
        "number of neighbors drawn in imitation",
        "(Dict of) number of neighbors drawn for each imitating entity. Only applicable for type='threshold'. Alternatively, imi_p_drawn can be specified, but not both.",
        datatype = Union[int, Dict[str, int]],
        unit=D.unity, quantum=1, lower_bound=0, allow_none=True, default=None)

    imi_p_neighbor_drawn = Variable(
        "probabilities of neighbors being drawn in imitation",
        "(Dict of) probabilities with which each neighbor is drawn. Only applicable for type='threshold'. Alternatively, imi_n_neighbors_drawn can be specified, but not both.",
        datatype = Union[float, Dict[str, float]],
        unit=D.unity, lower_bound=0, upper_bound=1, allow_none=True, default=None)

    imi_abs_threshold = Variable(
        "absolute imitation thresholds",
        "(Dict of (dict of)) number of drawn neighbors having target value needed for imitation if imitating entity has source value. Only applicable for type='threshold'. Alternatively, imi_rel_threshold can be specified, but not both. If dict of dict, inner dict keys must be of the form (source value, target value), where both source and target values might be '*' to indicate that this entry applies to all source or target values.",
        datatype = Union[int, Dict[str, int], Dict[str, Dict[Tuple[Any, Any], int]]],
        unit=D.unity, quantum=1, lower_bound=0, allow_none=True, default=None)

    imi_rel_threshold = Variable(
        "relative imitation thresholds",
        "(Dict of (dict of)) fraction of drawn neighbors having target value needed for imitation if imitating entity has source value. Only applicable for type='threshold'. Alternatively, imi_abs_threshold can be specified, but not both. If dict of dict, inner dict keys must be of the form (source value, target value), where both source and target values might be '*' to indicate that this entry applies to all source or target values.",
        datatype = Union[float, Dict[str, float], Dict[str, Dict[Tuple[Any, Any], float]]],
        unit=D.unity, lower_bound=0, upper_bound=1, allow_none=True, default=None)
    
    
    # interface method for triggering imitation:
    
    def trigger_imitation(self, key="*"):
        """Trigger the imitation of some (group of) variable(s). 
        Will automatically be called at the rates specified in Culture.imi_rates, 
        but can be called independently to trigger imitation, e.g. based on certain events.
        :param key: key of the (group of) variable(s) to imitate, as specified in Culture.imi_traits. If '*', imitate everything in imi_traits.
        :type key: str, optional
        """
        pass
        
    