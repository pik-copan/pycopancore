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
from ...data_model.master_data_model import I
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "generic imitation of traits on networks"
    """a unique name for the model component"""
    description = """
For each of a list of traits (=combinations of variables), a certain fraction 
of entities of the variable's owning type looks at a certain number of fraction 
of their neighbors on a certain network and imitates their variable values with 
certain probabilities when certain thresholds are met.

All these specifics are governed by parameters in Culture that can be 
overridden in imitating entity types by providing respective variables or 
methods there.
  E.g., to override the imitation rate for the trait with key 'tax', the entity 
type can either define a Variable or method named imi_rate_tax.

To use this component, the model composer must first import 
model_components.config, then set config.generic_imitation['variables'] to a 
list of variables that this component shall act on, and only then import 
model_components.generic_imitation.
  Each entry in config.generic_imitation['variables'] must be a dot construct 
starting at base.interface.Culture and leading to the variable in question.
  E.g., if the variables Individual.is_environmentally_friendly and 
SocialSystem.emissions_tax_level shall be imitated, put 
config.generic_imitation['variables'] = 
[base.interface.Culture.individuals.is_environmentally_friendly, 
base.interface.Culture.social_systems.emissions_tax_level].

For details about the implemented imitation process, see
:doc:`here<./docs/index.md>`
"""
    """some longer description"""
    requires = ['config']
    """list of other model components required for this model component to
    make sense"""


# process taxa:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # exogenous variables / parameters:
        
    imi_traits = Variable(
        "imitated variable traits",
        "Dict of key: trait. Each trait is a tuple of one or more Variables that shall be imitated together. " \
        "Each occurring Variable must also be listed in the config variable generic_imitation['variables']. " \
        "See this model component's Model.description for more information on this. " \
        "All other imi_* parameters defined in Culture are allowed to be dictionaries keyed with the keys listed here, " \
        "or with the key '*' for specifying values to be applied to all (other) entries occurring here. " \
        "For some of them, their values can also be overridden by imitating entity types " \
        "by providing variables or methods named imi_p_imitate_<key>, imi_p_imitate_<key> etc.",
        datatype = Dict[str, Tuple[Variable]], 
        default={})

    # settings that cannot be overridden:

    imi_rate = Variable(
        "imitation rate",
        "(Dict of) rates at which a batch of entities imitates.",
        datatype = Union[float, Dict[str, float]],
        unit=D.years**-1, lower_bound=0, default=0)
    # NOTE: imitation can also be triggered from other components by calling ...
            
    imi_type = Variable(
        "imitation type",
        "(Dict of) string(s) specifying the type(s) of imitation: " \
        "'simple' means entities draw one neighbor and imitate it with some probability. " \
        "'complex' means entities draw several neighbors " \
        "and imitate each observed value occurring above a certain threshold with some probability.",
        datatype = Union[str, Dict[str, str]],
        scale='nominal', levels=['simple', 'complex'], default='simple')

    imi_network = Variable(
        "imitation network",
        "(Dict of) Variable object(s) containing the network(s) imitation is based on.",
        datatype = Union[Graph, DiGraph, Dict[str, Union[Graph, DiGraph]]])
        
    imi_spreading_direction = Variable(
        "imitation spreading direction",
        "(Dict of) 'forward' or 'backward'. Only applicable if network is directed. " \
        "If 'forward', nodes imitate their predecessors. " \
        "If 'backward', nodes imitate their successors in the directed network",
        datatype = Union[str, Dict[str, str]], allow_none=True, default=None)

    imi_batch_n = Variable(
        "imitation batch size",
        "(Dict of) size(s) of batches imitating at the same time. " \
        "Alternatively, imi_p_in_batch can be specified, but not both.",
        datatype = Union[int, Dict[str, int]],
        unit=D.unity, quantum=1, lower_bound=0, allow_none=True, default=None)
        
    # parameters that can be overridden by entities:

    imi_p_in_batch = Variable(
        "probability of being in an imitation batch",
        "(Dict of) probability/ies with which entities are selected to be in an imitation batch. " \
        "Alternatively, imi_batch_n can be specified, but not both. " \
        "Can be overridden by imitating entity types by providing " \
        "variables or methods named imi_p_in_batch_<key> " \
        "where <key> is a trait key defined in imi_traits.",
        datatype = Union[float, Dict[str, float]],
        unit=D.unity, lower_bound=0, upper_bound=1, allow_none=True, default=None)
    
    imi_include_own_trait = Variable(
        "include own trait",
        "(Dict of) boolean value specifying whether the imitating entity's own trait " \
        "shall be considered a candidate trait as well." \
        "Can be overridden by imitating entity types by providing " \
        "variables or methods named imi_include_own_trait_<key> " \
        "where <key> is a trait key defined in imi_traits. ",
        datatype = Union[bool, Dict[str, bool]])

    imi_delta = Variable(
        "imitation evaluation delta",
        "(Dict of) delta value(s) used in selecting the nominated trait. " \
        "Can be overridden by imitating entity types by providing " \
        "variables or methods named imi_delta_<key> " \
        "where <key> is a trait key defined in imi_traits.",
        unit=D.unity, lower_bound=0, allow_none=True, default=None)
    
    imi_p_imitate = Variable(
        "imitation probability",
        "(Dict of (dict of)) probability/ies to actually imitate the candidate value (in the 'simple' case, the value of a randomly drawn neighbor, in the 'threshold' case, each value occurring in the drawn neighbors more often than the thresholds say). " \
        "If dict of dict, inner dict keys must be of the form (source value, target value), where both source and target values are trait value tuples or might be '*' to indicate that this entry applies to all source or target values. " \
        "Can be overridden by imitating entity types by providing variables or methods named imi_p_imitate_<key> where <key> is a trait key defined in imi_traits. " \
        "If overridden by a method, that method must accept the named arguments other=, own_trait=, and other_trait=.",
        datatype = Union[float, Dict[str, float], Dict[str, Dict[Tuple[Any, Any], float]]],
        unit=D.unity, lower_bound=0, upper_bound=1, default=1)
        
    # only applicable to type='threshold':
    
    imi_n_neighbors_drawn = Variable(
        "number of neighbors drawn in imitation",
        "(Dict of) number of neighbors drawn for each imitating entity. " \
        "Only applicable for type='threshold'. " \
        "Alternatively, imi_p_drawn can be specified, but not both. " \
        "Can be overridden by imitating entity types by providing a variables or methods named imi_n_neighbors_drawn_<key> where <key> is a trait key defined in imi_traits. ",
        datatype = Union[int, Dict[str, int]],
        unit=D.unity, quantum=1, lower_bound=0, allow_none=True, default=None)

    imi_p_neighbor_drawn = Variable(
        "probability of neighbors being drawn in imitation",
        "(Dict of) probability/ies with which each neighbor is drawn. " \
        "Only applicable for type='threshold'. " \
        "Alternatively, imi_n_neighbors_drawn can be specified, but not both. " \
        "Can be overridden by imitating entity types by providing a variables or methods named imi_p_neighbor_drawn_<key> where <key> is a trait key defined in imi_traits. " \
        "If overridden by a method, that method must accept the named argument neighbor=.",
        datatype = Union[float, Dict[str, float]],
        unit=D.unity, lower_bound=0, upper_bound=1, allow_none=True, default=None)

    imi_abs_threshold = Variable(
        "absolute imitation threshold",
        "(Dict of (dict of)) number(s) of drawn neighbors having target value needed for imitation if imitating entity has source value. " \
        "Only applicable for type='threshold'. " \
        "Alternatively, imi_rel_threshold can be specified, but not both. " \
        "If dict of dict, inner dict keys must be of the form (source value, target value), where both source and target values are trait value tuples or might be '*' to indicate that this entry applies to all source or target values. " \
        "Can be overridden by imitating entity types by providing a variables or methods named imi_abs_threshold_<key> where <key> is a trait key defined in imi_traits. " \
        "If overridden by a method, that method must accept the named arguments other=, own_trait=, other_trait=.",
        datatype = Union[int, Dict[str, int], Dict[str, Dict[Tuple[Any, Any], int]]],
        unit=D.unity, quantum=1, lower_bound=0, allow_none=True, default=None)

    imi_rel_threshold = Variable(
        "relative imitation threshold",
        "(Dict of (dict of)) fraction(s) of drawn neighbors having target value needed for imitation if imitating entity has source value. " \
        "Only applicable for type='threshold'. " \
        "Alternatively, imi_abs_threshold can be specified, but not both. " \
        "If dict of dict, inner dict keys must be of the form (source value, target value), where both source and target values are trait value tuples or might be '*' to indicate that this entry applies to all source or target values. " \
        "Can be overridden by imitating entity types by providing a variables or methods named imi_rel_threshold_<key> where <key> is a trait key defined in imi_traits. " \
        "If overridden by a method, that method must accept the named arguments other=, own_trait=, other_trait=.",
        datatype = Union[float, Dict[str, float], Dict[str, Dict[Tuple[Any, Any], float]]],
        unit=D.unity, lower_bound=0, upper_bound=1, allow_none=True, default=None)
    
    
    # interface method for triggering imitation:
    
    def trigger_imitation(self, key="*"):
        """Trigger the imitation of some (group of) variable(s). 
        
        Will automatically be called at the rates specified in Culture.imi_rate, 
        but can be called independently to trigger imitation, e.g. based on certain events.
        
        Parameters
        ----------
        key : str, optional
            Key of the (group of) variable(s) to imitate, as specified in Culture.imi_traits. If '*', imitate everything in imi_traits
        """
        pass
        
    
