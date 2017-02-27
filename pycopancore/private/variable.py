"""A class to define model variables and inherits from Symbol.

Each Varible is connected to an entity, of which it is a variable.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from sympy import Symbol
from pycopancore.data_model import DimensionalQuantity


class Variable (Symbol):
    """Define the Variable Class."""

    # standard metadata:
    
    name = None # human-readable name to be used as label etc.
    desc = None # longer description text
    symbol = None # mathematical symbol or abbrev. to be used as a short label
    reference = None # some URI, e.g. a wikipedia page
    
    # level of measurement: "ratio" (default), "interval", "ordinal", 
    # or "nominal" (see https://en.wikipedia.org/wiki/Level_of_measurement):
    scale = None
    
    default = None # default initial value
    uninformed_prior = None # random value generator (prob. distrib.)
     
    datatype = None # e.g. float, integer, numpy.ndarray, networkx.Graph, ...
    lower_bound = None # inclusive
    strict_lower_bound = None # exclusive
    upper_bound = None # inclusive
    strict_upper_bound = None # exclusive
    quantum = None # values must be integer multiples of this
    
    # scale-specific metadata:

    # if "ratio" or "interval":
    unit = None # a pycopancore.data_model.Unit

    # if "ordinal" or "nominal":
    levels = None # values must be element of this
    
    # attributes needed for internal framework logics:

    owning_classes = []
    _codename = None

    
    # standard methods:

    def __init__(self,
                 name,
                 desc,
                 *,
                 symbol=None,
                 reference=None,
                 scale="ratio",
                 default=None,
                 uninformed_prior=None,
                 datatype=float,
                 lower_bound=None,
                 strict_lower_bound=None,
                 upper_bound=None,
                 strict_upper_bound=None,
                 quantum=None,
                 unit=None,
                 levels=None,
                 ):
        super().__init__()
        
        self.name = name
        self.desc = desc
        self.symbol = symbol
        self.reference = reference
        
        assert scale in ("ratio", "interval", "ordinal", "nominal"), \
            "scale must be ratio, interval, ordinal, or nominal"
        self.scale = scale
        
        self.default = default
        self.uninformed_prior = uninformed_prior
        
        self.datatype = datatype
        self.lower_bound = lower_bound
        self.strict_lower_bound = strict_lower_bound
        self.upper_bound = upper_bound
        self.strict_upper_bound = strict_upper_bound
        self.quantum = quantum
        self.unit = unit
        self.levels = levels
        
  
    # validation:
    
    def _check_valid(self, v):
        """check validity of candidate value"""
        
        if self.datatype is not None:
            if not isinstance(v, self.datatype):
                return False, "must be instance of " + str(self.datatype)
            
        if self.lower_bound is not None:
            if not v >= self.lower_bound: 
                return False, "must be >= " + str(self.lower_bound)

        if self.strict_lower_bound is not None:
            if not v > self.strict_lower_bound: 
                return False, "must be > " + str(self.strict_lower_bound)

        if self.upper_bound is not None:
            if not v <= self.upper_bound: 
                return False, "must be <= " + str(self.upper_bound)

        if self.strict_upper_bound is not None:
            if not v < self.strict_upper_bound: 
                return False, "must be < " + str(self.strict_upper_bound)
            
        if self.quantum is not None:
            if not v % quantum == 0:
                return False, "must be integer multiple of " \
                                + str(self.quantum)

        if self.levels is not None:
            if not v in levels:
                return False, "must be in " \
                                + str(self.levels)

    def is_valid(self, value):
        if isinstance(value, DimensionalQuantity):
            value = value.multiple(unit=self.unit)
        return self._check_valid(value) == True
    
    def assert_valid(self, value):
        """Make sure by assertion that value is valid"""
        res = self._check_valid(value)
        assert res == True, res[1]


    # "getters" and "setters":

    def set_value(self, entity, value):
        """Set value for some entity,
        possibly performing conversion to correct unit
        if value is a DimensionalQuantity,
        otherwise using own default unit"""
        if isinstance(value, DimensionalQuantity):
            value = value.multiple(unit=self.unit)
        self.assert_valid(value)
        entity.__dict__[self._codename] = value
        
    def set_to_default(self,
                       entities=None, # if None: all entities/taxa
                       ):
        """Set values in selected entities to default"""
        if entities is not None:
            for e in entities:
                self.set_value(e, self.default)
        else:
            for c in self.owning_classes:
                for e in c.entities:
                    self.set_value(e, self.default)
        
    def set_to_random(self,
                      entities=None, # if None: all entities/taxa
                      distribution=None, # if None: self.uninformed_prior
                      ):
        """Set values in selected entities to default"""
        if distribution is None:
            distribution = self.uninformed_prior
        if entities is not None:
            for e in entities:
                self.set_value(e, distribution())
        else:
            for c in self.owning_classes:
                for e in c.entities:
                    self.set_value(e, distribution())
        
    def set_values(self,
                   *,
                   dict=None,
                   entities=None,
                   values=None
                   ):
        """Set values for the variable.

        This function set values for the variable. If given a list of entities,
        it sets values for all of them.

        Parameters
        ----------
        dict : dict
            Optional dictionary of variable values keyed by Entity
            object (e.g. {cell:location, individual:age}, ...)
        entities : list
            Optional list of entities (Cells, Individuals, ...)
        values : list/array
            Optional corresponding list or array of values

        Returns
        -------

        """
        if dict is not None:
            for (e, v) in dict.items():

                #
                # Following assert statements need _AbstractEntityMixin. We
                # maybe should move them into the test environment:
                # assert isinstance(e, _AbstractEntityMixin), /
                # "key is not a model entity"
                # assert self._codename in e.__dict__, /
                # "variable is not contained in entity"
                #

                self.set_value(e, v)

        if entities is not None:
            for i in range(len(entities)):
                e = entities[i]

                #
                # as above...
                # assert isinstance(e, _AbstractEntityMixin). /
                # "key is not a model entity"
                # assert self._codename in e.__dict__, /
                # "variable is not contained in entity"
                #

                self.set_value(e, values[i])

    def clear_derivatives(self,
                          *,
                          entities=None
                          ):
        """Set all derivatives to zero.

        Parameters
        ----------
        entities : list
            List of the entities

        Returns
        -------

        """
        for e in entities:
            e.__dict__['d_'+self._codename] = 0

    def get_derivatives(self,
                        *,
                        entities=None
                        ):
        """Return a list of derivatives saved in entities.

        Parameters
        ----------
        entities : list
            List of the entities

        Returns
        -------

        """
        return[e.__dict__['d_'+self._codename] for e in entities]

    def get_value_list(self,
                       entities=None,
                       ):
        """Return values for given entities.

        Parameters
        ----------
        entities: list
            List of entities

        Returns
        -------
        List of variable value of each entity
        """
        return [e.__dict__[self._codename] for e in entities]
