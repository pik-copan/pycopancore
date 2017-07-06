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

import random
from sympy import Symbol

from . import DimensionalQuantity
from .. import private


EPS = 1e-10
"""infinitesimal value for ensuring strict bounds"""


class Variable (Symbol):
    """Metadata object representing a model variable or parameter."""

    # standard metadata:

    name = None
    """human-readable name to be used as label etc."""
    desc = None
    """longer description text"""
    symbol = None
    """mathematical symbol or abbrev. to be used as a short label"""
    ref = None
    """some URI, e.g. a wikipedia page"""

    scale = None
    """level of measurement: "ratio" (default), "interval", "ordinal",
    or "nominal" (see https://en.wikipedia.org/wiki/Level_of_measurement)"""

    default = None
    """default initial value"""
    uninformed_prior = None
    """random value generator (probability distribution) 
    if nothing else is known about the value"""

    # catalog references:

    CF = None
    """corresponding CF Standard Name
    (http://cfconventions.org/Data/cf-standard-names)"""
    AMIP = None
    """corresponding AMIP2 variable name
    (http://pcmdi.github.io/projects/amip/OUTPUT/AMIP2/outlist.html)"""
    IAMC = None
    """corresponding IAMC variable name
    (https://tntcat.iiasa.ac.at/ADVANCEWP1DB/static/download/Diagnostics_template_2015-08-12.xlsx)"""
    CETS = None
    """corresponding World Bank CETS code
    (https://databank.worldbank.org/data/download/site-content/WDI_CETS.xls)"""


    # data type and constraints:

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

    owning_class = None
    """the class owning the Variable as its attribute"""
    codename = None
    """the attribute name of the Variable in its owning class"""

    _uid = None
    """unique id"""

    # standard methods:

    # inheritance from Symbol is a little tricky since Symbol has a custom
    # __new__ method that returns the same object everytime the name is the
    # same! We break this behaviour by using random Symbol.names so that we
    # can multiple copies of a Variable having the same name, to be attached
    # to different entity types:
    @staticmethod
    def __new__(cls, name, *args, **assumptions):
        return super().__new__(cls,
                               str(random.random()),
                               **assumptions)

    def __init__(self,
                 name,
                 desc,
                 *,
                 symbol=None,
                 ref=None,
                 scale="ratio",
                 default=None,
                 uninformed_prior=None,
                 CF=None,
                 AMIP=None,
                 IAMC=None,
                 CETS=None,
                 datatype=(float,int),
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

        # store unique "name" given by sympy in _uid:
        self._uid = self.name

        self.name = name
        self.desc = desc
        self.symbol = symbol
        self.ref = ref

        assert scale in ("ratio", "interval", "ordinal", "nominal"), \
            "scale must be ratio, interval, ordinal, or nominal"
        self.scale = scale

        self.default = default
        self.uninformed_prior = uninformed_prior

        self.CF = CF
        self.AMIP = AMIP
        self.IAMC = IAMC
        self.CETS = CETS

        self.datatype = datatype
        self.array_shape = array_shape
        self.allow_none = allow_none
        self.lower_bound = lower_bound
        self.strict_lower_bound = strict_lower_bound
        self.upper_bound = upper_bound
        self.strict_upper_bound = strict_upper_bound
        self.quantum = quantum
        self.unit = unit

        assert not (is_extensive is True and is_intensive is True), \
                        "cannot be both extensive and intensive"
        self.is_extensive = is_extensive
        self.is_intensive = is_intensive

        self.levels = levels

    def __eq__(self, other):
        return object.__eq__(self, other)

    def copy(self):
        # TODO: do this more elegantly??
        c = Variable(self.name,
                     self.desc,
                     symbol=self.symbol,
                     ref=self.ref,
                     scale=self.scale,
                     default=self.default,
                     uninformed_prior=self.uninformed_prior,
                     CF=self.CF,
                     AMIP=self.AMIP,
                     IAMC=self.IAMC,
                     CETS=self.CETS,
                     datatype=self.datatype,
                     array_shape=self.array_shape,
                     allow_none=self.allow_none,
                     lower_bound=self.lower_bound,
                     strict_lower_bound=self.strict_lower_bound,
                     upper_bound=self.upper_bound,
                     strict_upper_bound=self.strict_upper_bound,
                     quantum=self.quantum,
                     unit=self.unit,
                     is_extensive=self.is_extensive,
                     is_intensive=self.is_intensive,
                     levels=self.levels
                     )
        return c

    def __hash__(self):
        return object.__hash__(self)

    def __str__(self):
        return (self.owning_class.__name__ + "." + self.codename) \
                if self.owning_class \
                else self.name

    def __repr__(self):
        return (self.owning_class.__name__ + "." + self.codename) \
                if self.owning_class \
                else self.name + " (" + self._uid + ")"
        # dirty fix for lengthy output 
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
                return False, \
                    str(self) + " array shape must be " + str(self.array_shape)
            for item in v:
                res = self._check_valid(item)
                if res is not True:
                    return res

        if v is None:
            if self.allow_none is False:
                return False, str(self) + " may not be None"
        else:
            if self.datatype is not None:
                if not isinstance(v, self.datatype):
                    return False, \
                        str(self) + " must be instance of " + str(self.datatype)

            if self.lower_bound is not None:
                if not v >= self.lower_bound:
                    return False, \
                        str(self) + " must be >= " + str(self.lower_bound)

            if self.strict_lower_bound is not None:
                if not v > self.strict_lower_bound:
                    return False, \
                        str(self) + " must be > " + str(self.strict_lower_bound)

            if self.upper_bound is not None:
                if not v <= self.upper_bound:
                    return False, \
                        str(self) + " must be <= " + str(self.upper_bound)

            if self.strict_upper_bound is not None:
                if not v < self.strict_upper_bound:
                    return False, \
                        str(self) + " must be < " + str(self.strict_upper_bound)

            if self.quantum is not None:
                if not v % self.quantum == 0:
                    return False, \
                        str(self) + " must be integer number of " \
                        + str(self.quantum)

            if self.levels is not None:
                if v not in self.levels:
                    return False, \
                        str(self) + " must be in " + str(self.levels)

        return True

    def is_valid(self, value):
        if isinstance(value, DimensionalQuantity):
            value = value.number(unit=self.unit)
        return self._check_valid(value) == True

    def assert_valid(self, value):
        """Make sure by assertion that value is valid"""
        res = self._check_valid(value)
        assert res is True, res[1]

    # "getters" and "setters":

    def set_value(self, instance, value):
        """Set value for some instance,
        possibly performing conversion to correct unit
        if value is a DimensionalQuantity,
        otherwise using own default unit"""
        if isinstance(value, DimensionalQuantity):
            value = value.number(unit=self.unit)
#        self.assert_valid(value)
        setattr(instance, self.codename, value)

    def __setitem__(self, instance, value):
        """magic method allowing access to instance values via var[instance]"""
        return self.set_value(instance, value)

    def convert_to_standard_units(self,
                                  instances=None,  # if None: all entities/taxa
                                  ):
        """replace all variable values of type DimensionalQuantity
        to float using the standard unit"""
        if instances is not None:
            for i in instances:
                v = getattr(i, self.codename)
                if isinstance(v, DimensionalQuantity):
                    self.set_value(i, v)  # does the conversion
        else:
            for i in self.owning_class.instances:
                v = getattr(i, self.codename)
                if isinstance(v, DimensionalQuantity):
                    self.set_value(i, v)  # does the conversion

    def _get_instances(self, instances):
        """converts argument into a set of instances
        (entities or process taxa)"""
        if instances is None: # use all that have this variable
            instances = self.owning_class.instances
        elif isinstance(instances, dict): # use all that appear in keys or values
            instances = set()
            for k,i in instances.keys():
                instances.update(self._get_instances(k))
                instances.update(self._get_instances(i))
        elif isinstance(instances,
                        (private._AbstractEntityMixin,
                         private._AbstractProcessTaxonMixin)):
            instances = set([instances])
        else:
            instances = set(instances)
        return instances

    def set_to_default(self,
                       instances=None,  # if None: all entities/taxa
                       ):
        """Set values in selected entities to default"""
        instances = self._get_instances(instances)
        for e in instances:
            self.set_value(e, self.default)

    def set_to_random(self,
                      instances=None,  # if None: all entities/taxa
                      distribution=None,  # if None: self.uninformed_prior
                      *,
                      p=1
                      ):
        """Set values in selected entities to random value.
        If distribution=None, use uninformed_prior.
        If optional p is given, replace current value only with probability p."""
        if distribution is None:
            distribution = self.uninformed_prior
        instances = self._get_instances(instances)
        for i in instances:
            if random.random() < p:
                self.set_value(i, distribution())

    def add_noise(self,
                  instances=None,  # if None: all entities/taxa
                  distribution=random.gauss, # basic noise distribution
                  *,
                  factor=1, # scale factor
                  offset=0, # location offset
                  multiplicative=False
                  ):
        """Set values in selected entities to random value.
        If distribution=None, use uninformed_prior.
        If optional p is given, replace current value only with probability p."""
        assert self.scale in ("ratio", "interval"), \
                "can only add noise to ratio or interval scaled variables"
        instances = self._get_instances(instances)
        for i in instances:
            v = self.get_value(i)
            noise = factor * distribution() + offset
            if multiplicative:
                v *= noise
            else:
                v += noise
            # enforce bounds and quantization
            if self.lower_bound is not None:
                v = max(v, self.lower_bound)
            if self.strict_lower_bound is not None:
                v = max(v, self.strict_lower_bound + EPS)
            if self.upper_bound is not None:
                v = min(v, self.upper_bound)
            if self.strict_upper_bound is not None:
                v = min(v, self.strict_upper_bound - EPS)
            if self.quantum is not None:
                v = round(v / self.quantum) * self.quantum
            # TODO: deal with possible interferences between bounds and quantum
            self.set_value(i, v)

    def fast_set_values(self, values):
        """fast-track method to set values without checks and conversions"""
        cn = self.codename
        if values.size > 1:
            for i, inst in enumerate(self.owning_class.instances):
                setattr(inst, cn, values[i])
        else:
            for inst in self.owning_class.instances:
                setattr(inst, cn, values[0])

    def set_values(self,
                   instances=None,
                   values=None,
                   *,
                   dictionary=None
                   ):
        """Set values for the variable.

        This function set values for the variable. If given a list of entities,
        it sets values for all of them.

        Parameters
        ----------
        dictionary : dictionary
            Optional dictionary of variable values keyed by Entity
            object (e.g. {cell:location, individual:age}, ...)
        instances : list
            List of entities/process taxa
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
                # assert hastattr(e, self.codename), /
                # "variable is not contained in entity"
                #

                self.set_value(e, v)

        for i, inst in enumerate(instances):
            self.set_value(inst, values[i])

    def clear_derivatives(self,
                          *,
                          instances=None
                          ):
        """Set all derivatives to zero.

        Parameters
        ----------
        instances : list
            List of the entities

        Returns
        -------

        """
        instances = self._get_instances(instances)
        for i in instances:
            setattr(i, 'd_'+self.codename, 0)

    def get_derivatives(self,
                        instances=None
                        ):
        """Return a list of derivatives saved in entities.

        Parameters
        ----------
        instances : list
            List of entities/process taxa

        Returns
        -------

        """
        return [getattr(i, 'd_'+self.codename) for i in instances]

    def get_value(self, instance, unit=None):
        v = getattr(instance, self.codename)
        assert not isinstance(v, Variable), \
            "Variable " + str(self) + " uninitialized at instance " \
            + str(instance)
        return v if unit is None else self._unit.convert(v, unit)

    def __getitem__(self, instance):
        """magic method allowing access to instance values via var[instance]"""
        return self.get_value(instance)

    def eval(self,
                   instances=None,
                   *,
                   unit=None
                   ):
        """Return values for given entities,
        optionally in a different unit.

        Parameters
        ----------
        instances: iterable
            List of entities/process taxa

        Returns
        -------
        List of variable value of each entity
        """
#        return [self.get_value(inst, unit=unit) for inst in instances]  # too slow...
        if instances is None:
            instances = self.owning_class.instances
        if unit is None:
            cn = self.codename
            return [getattr(inst, cn) for inst in instances]
        else:
            return [self.get_value(inst, unit=unit) for inst in instances]

    @property  # read-only
    def target_class(self):
        return self.owning_class

    @property  # read-only
    def target_variable(self):
        return self

    @property  # read-only
    def target_instances(self):
        return self.owning_class.instances

    # stuff needed if Variable occurs as arg of _DotConstruct:
    @property  # read-only
    def branchings(self):
        return [[len(self.owning_class.instances)]]

    @property  # read-only
    def cardinalities(self):
        return [1, len(self.owning_class.instances)]

