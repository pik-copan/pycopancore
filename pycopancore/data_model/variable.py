"""A class to define model variables, inherits from Symbol.

Each Variable can be connected to any number of entity types and/or process
taxa.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from sympy import Symbol
from pycopancore.data_model import DimensionalQuantity


class Variable (Symbol):
    """Define the Variable Class."""

    # standard metadata:

    name = None
    """human-readable name to be used as label etc."""
    desc = None
    """longer description text"""
    symbol = None
    """mathematical symbol or abbrev. to be used as a short label"""
    reference = None
    """some URI, e.g. a wikipedia page"""

    scale = None
    """level of measurement: "ratio" (default), "interval", "ordinal",
    or "nominal" (see https://en.wikipedia.org/wiki/Level_of_measurement)"""

    default = None
    """default initial value"""
    uninformed_prior = None
    """random value generator (probability distribution) 
    if nothing else is known about the value"""

    datatype = None
    """e.g. float, integer, numpy.ndarray, networkx.Graph, ..."""
    array_shape = None
    """if numpy array, specifies its shape"""
    allow_none = None
    """whether None is an allowed value"""
    lower_bound = None
    """(inclusive, value must be >=)"""
    strict_lower_bound = None
    """(exclusive, value must be >)"""
    upper_bound = None
    """(inclusive, value must be <=)"""
    strict_upper_bound = None
    """(exclusive, value must be <)"""
    quantum = None
    """values must be integer multiples of this"""

    # scale-specific metadata:

    unit = None
    """a pycopancore.data_model.Unit (only for ratio- or interval-scaled)"""
    is_extensive = None
    """whether variable scales proportionally with system size
    (only for ratio-scaled)"""
    is_intensive = None
    """whether variable must remain invariant when doubling system"""

    # if "ordinal" or "nominal":
    levels = None  # values must be element of this

    # attributes needed for internal framework logics:

    owning_classes = []
    _codename = None

    # standard methods:

    # inheritance from Symbol is a little tricky since Symbol has a custom
    # __new__ method:
    @staticmethod
    def __new__(cls, name, *args, **assumptions):
        return super().__new__(cls, name, **assumptions)

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
                 array_shape=None,
                 allow_none=True,  # by default, var may be none
                 lower_bound=None,
                 strict_lower_bound=None,
                 upper_bound=None,
                 strict_upper_bound=None,
                 quantum=None,
                 unit=None,
                 is_extensive=False,
                 is_intensive=False,
                 levels=None,
                 **kwargs
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
        self.array_shape = array_shape
        self.allow_none = allow_none
        self.lower_bound = lower_bound
        self.strict_lower_bound = strict_lower_bound
        self.upper_bound = upper_bound
        self.strict_upper_bound = strict_upper_bound
        self.quantum = quantum
        self.unit = unit
        self.is_extensive = is_extensive
        self.is_intensive = is_intensive
        self.levels = levels

    def __repr__(self):
        r = "Variable " + self.name + "(" + self.desc + "), scale=" \
            + self.scale + ", datatype=" + str(self.datatype)
        if self.unit is not None:
            r += ", unit=" + str(self.unit)
        if self.default is not None:
            r += ", default=" + str(self.default)
        if self.allow_none is False:
            r += ", not None"
        if self.lower_bound is not None:
            r += ", >=" + str(self.lower_bound)
        if self.strict_lower_bound is not None:
            r += ", >" + str(self.strict_lower_bound)
        if self.upper_bound is not None:
            r += ", <=" + str(self.upper_bound)
        if self.strict_upper_bound is not None:
            r += ", <" + str(self.strict_upper_bound)
        if self.quantum is not None:
            r += ", % " + str(self.quantum) + " == 0"
        if self.levels is not None:
            r += ", levels=" + str(self.levels)
        if self.array_shape is not None:
            r += ", shape=" + str(self.array_shape)
        return r

    # validation:

    def _check_valid(self, v):
        """check validity of candidate value"""

        if self.array_shape is not None:
            if not v.shape == self.array_shape:
                return False, "array shape must be " + str(self.array_shape)
            for item in v:
                res = self._check_valid(item)
                if res is not True:
                    return res

        if v is None:
            if self.allow_none is False:
                return False, "may not be None"
        else:
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
                if not v % self.quantum == 0:
                    return False, "must be integer multiple of " \
                                    + str(self.quantum)

            if self.levels is not None:
                if v not in self.levels:
                    return False, "must be in " + str(self.levels)

        return True

    def is_valid(self, value):
        if isinstance(value, DimensionalQuantity):
            value = value.multiple(unit=self.unit)
        return self._check_valid(value) == True

    def assert_valid(self, value):
        """Make sure by assertion that value is valid"""
        res = self._check_valid(value)
        assert res is True, res[1]

    # "getters" and "setters":

    def set_value(self, entity, value):
        """Set value for some entity,
        possibly performing conversion to correct unit
        if value is a DimensionalQuantity,
        otherwise using own default unit"""
        if isinstance(value, DimensionalQuantity):
            value = value.multiple(unit=self.unit)
        self.assert_valid(value)
        setattr(entity, self._codename, value)

    def convert_to_standard_units(self,
                                  entities=None,  # if None: all entities/taxa
                                  ):
        """replace all variable values of type DimensionalQuantity
        to float using the standard unit"""
        if entities is not None:
            for e in entities:
                v = getattr(e, self._codename)
                if isinstance(v, DimensionalQuantity):
                    self.set_value(e, v)  # does the conversion
        else:
            for c in self.owning_classes:
                for e in c.entities:
                    v = getattr(e, self._codename)
                    if isinstance(v, DimensionalQuantity):
                        self.set_value(e, v)  # does the conversion

    def set_to_default(self,
                       entities=None,  # if None: all entities/taxa
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
                      entities=None,  # if None: all entities/taxa
                      distribution=None,  # if None: self.uninformed_prior
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
                   dictionary=None,
                   entities=None,
                   values=None
                   ):
        """Set values for the variable.

        This function set values for the variable. If given a list of entities,
        it sets values for all of them.

        Parameters
        ----------
        dictionary : dictionary
            Optional dictionary of variable values keyed by Entity
            object (e.g. {cell:location, individual:age}, ...)
        entities : list
            Optional list of entities (Cells, Individuals, ...)
        values : list/array
            Optional corresponding list or array of values

        Returns
        -------

        """
        if dictionary is not None:
            for (e, v) in dictionary.items():

                #
                # Following assert statements need _AbstractEntityMixin. We
                # maybe should move them into the test environment:
                # assert isinstance(e, _AbstractEntityMixin), /
                # "key is not a model entity"
                # assert hastattr(e, self._codename), /
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
                # assert hastattr(e, self._codename), /
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
            setattr(e, 'd_'+self._codename, 0)

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
        return [getattr(e, 'd_'+self._codename) for e in entities]

    def get_value_list(self,
                       entities=None,
                       unit=None
                       ):
        """Return values for given entities,
        optionally in a different unit.

        Parameters
        ----------
        entities: list
            List of entities

        Returns
        -------
        List of variable value of each entity
        """
        l = [getattr(e, self._codename) for e in entities]
        return l if unit is None else self._unit.convert(l, unit)
