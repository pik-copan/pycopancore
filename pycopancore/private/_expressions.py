'''
Created on Mar 20, 2017

@author: heitzig
'''

# defines logics to deal with symbolic expressions and their evaluation

import random
import numpy as np
import sympy as sp

from .. import data_model as D
from .. import private

from numba import jit, njit


# hierarchical aggregation functions:

def aggregation(npfunc):

    @njit
    def _func(values, lens):
        values = np.array(values)
        results = np.zeros(len(lens))
        offset = 0
        for i in range(len(lens)):
            newoffset = offset + lens[i]
            results[i] = npfunc(values[offset:newoffset])
            offset = newoffset
        return list(results)

    def func(values,
             branchings  # list of list of branchings by descending level
             ):
        for lens in reversed(branchings):
            values = _func(values, lens)
        return values

    return func

a_sum,  a_mean,  a_std,  a_var,  a_min,  a_median,  a_max \
= map(aggregation, [ \
np.sum, np.mean, np.std, np.var, np.min, np.median, np.max
])

aggregation_names = \
    set(["sum", "mean", "std", "var", "min", "median", "max"])

# hierarchical broadcasting:

@njit
def _broadcast(values, lens):
    result = np.zeros(np.sum(np.array(lens)))
    offset = 0
    for i in range(len(lens)):
        newoffset = offset + lens[i]
        result[offset:newoffset] = values[i]
        offset = newoffset
    return list(result)

def broadcast(values, branchings):
    for lens in branchings:
        values = _broadcast(values, lens)
    return values


class _DotConstruct (sp.Symbol):
    """A _DotConstruct represents a syntactical construct with dots,
    starting with an entity-type or process taxon class,
    followed by zero or more ReferenceVariables or SetVariables 
    or aggregation keywords such as sum, and ending in either an attribute,
    e.g. Society.sum.cells.population
    or an aggregation keyword without evaluation,
    e.g. Society.world.sum,
    or an aggregation keyword with evaluation,
    e.g. Society.world.sum(some expression).
    """

    _owning_class_or_var = None
    """the entity-type of process taxon at the start of the dot construct,
    e.g. Society"""
    name_sequence = None
    """the sequence of further names,
    e.g. ["sum","cells","population"]"""
    arg = None
    """the optional argument of the aggregation function,
    e.g. Society.world.sum.cells.population * Society.world.sum.cells.capital"""
    can_be_target = None
    """whether this can be a target (e.g. does not involve aggregation)"""

    _uid = None
    """unique id"""

    # inheritance from Symbol is a little tricky since Symbol has a custom
    # __new__ method that returns the same object everytime the name is the
    # same! We break this behaviour by using random Symbol.names so that we
    # can multiple copies of a Variable having the same name, to be attached
    # to different entity types:
    @staticmethod
    def __new__(cls,
                owning_class_or_var,
                name_sequence,
                *args,
                arg=None,
                **assumptions):
        return super().__new__(cls,
                               str(owning_class_or_var)
                               + str(name_sequence)
                               + str(arg),
                               **assumptions)

    def __init__(self,
                 owning_class_or_var,
                 name_sequence,
                 arg=None
                 ):
        super().__init__()

        # store unique "name" given by sympy in _uid:
        self._uid = self.name

        self._owning_class_or_var = owning_class_or_var
        self.name_sequence = name_sequence
        self.arg = arg

        self.can_be_target = True
        for name in name_sequence:
            if name in aggregation_names:
                self.can_be_target = False
                break

        self._target_class = private.unknown
        self._target_variable = private.unknown
        self._target_instances = private.unknown
        self._branchings = private.unknown
        self._cardinalities = private.unknown

    def __getattr__(self, name):
        """accessing an attribute of a _DotConstruct simply
        returns a new _DotConstruct that is extended by the name of this
        attribute"""
        assert self.arg is None, "can't have a . behind a ) here"
        return _DotConstruct(self.owning_class,
                             self.name_sequence + [name])

    def __call__(self, *arg):
        assert self.arg is None, "can't have a ( behind a ) here"
        assert self.name_sequence[-1] in aggregation_names, \
                    self.name_sequence[-1] + " is not an aggregation keyword"
        return _DotConstruct(self.owning_class,
                             self.name_sequence,
                             arg=arg)

    def __repr__(self):
        repr = str(self.owning_class) + "." + ".".join(self.name_sequence)
        if self.arg is not None:
            repr += "(" + str(self.arg) + ")"
        return repr

    def __str__(self):
        return self.__repr__()

    @property  # read-only
    def target_class(self):
        """return the class owning the target attribute"""
        assert self.can_be_target, "cannot serve as target"
        if self._target_class is private.unknown:
            value = self.owning_class.instances[0]
            for name in self.name_sequence[:-1]:
                value = getattr(value, name)
                try:  # use first element if iterable:
                    value = next(iter(value))
                except:
                    pass
            self._target_class = value.__class__
        return self._target_class

    @property  # read-only
    def owning_class(self):
        if isinstance(self._owning_class_or_var, D.Variable):
            self.name_sequence[0] = self._owning_class_or_var.codename
            self._owning_class_or_var = self._owning_class_or_var.owning_class
        return self._owning_class_or_var

    @property  # read-only
    def target_variable(self):
        """return the Variable object representing the target attribute"""
        assert self.can_be_target, "cannot serve as target"
        if self._target_variable is private.unknown:
            self._target_variable = getattr(self.target_class,
                                            self.name_sequence[-1])
        return self._target_variable

    @property  # read-only
    def target_instances(self):
        """return the list of instances owning the referenced attributes,
        may contain instances more than once due to broadcasting"""
        assert self.can_be_target, "cannot serve as target"
        if self._target_instances is private.unknown:
            self._analyse_instances()
        return self._target_instances

    @property  # read-only
    def branchings(self):
        """return the list of branching lens at SetReferences,
        to be used in aggregation and broadcasting"""
        if self._target_instances is private.unknown:
            self._analyse_instances()
        return self._branchings

    @property  # read-only
    def cardinalities(self):
        """return the list of level cardinalities at SetReferences,
        to be used in aggregation and broadcasting"""
        if self._target_instances is private.unknown:
            self._analyse_instances()
        return self._cardinalities

    def _analyse_instances(self):
        print("(analysing instance structure of",self,")")
        items = self.owning_class.instances
        branchings = []
        cardinalities = [len(items)]  # store initial cardinality
        for name in self.name_sequence[:-1]:
            if name in aggregation_names:
                break
            if hasattr(items[0], "__iter__"):  # each item is a set of instances
                branchings.append([len(instance_set)
                                   for instance_set in items])
                items = [getattr(i, name)
                         for instance_set in items
                         for i in instance_set]
                cardinalities.append(len(items))  # store cardinality after the branching
            else:
                items = [getattr(i, name) for i in items]
                # items may now be a list of instances or a list of sets of instances...
        if hasattr(items[0], "__iter__"):
            items = [i
                     for instance_set in items
                     for i in instance_set]
        self._target_instances = items
        self._branchings = branchings
        self._cardinalities = cardinalities

    def eval(self, instances=None):
        """gets referenced attribute values and performs aggregations where necessary"""
        items = self.owning_class.instances if instances is None else instances
        for name in self.name_sequence:
            if name in aggregation_names:
                raise NotImplementedError
            if hasattr(items[0], "__iter__"):  # each value is a set of instances
                items = [getattr(i, name)
                         for instance_set in items
                         for i in instance_set]
            else:
                items = [getattr(i, name) for i in items]
        return items

    def _broadcast(self, values):
        """broadcast a list of values from entities at an intermediate level
        to their "offspring" entities at the final level"""
        value_level = self._cardinalities.index(len(values))
        if value_level < len(self.cardinalities) - 1:
            values = broadcast(values, self._branchings[value_level + 1:])
        return values

    def add_values(self, values):
        """adds summands to referenced attribute values"""
        assert self.can_be_target, "cannot serve as target"
        # broadcast values if necessary:
        values = self._broadcast(values)
        name = self.name_sequence[-1]
        for pos, i in enumerate(self.target_instances):
            setattr(i, name, getattr(i, name) + values[pos])

    def add_derivatives(self, values):
        """adds summands to referenced attribute values"""
        assert self.can_be_target, "cannot serve as target"
        # broadcast values if necessary:
        values = self._broadcast(values)
        dname = "d_" + self.name_sequence[-1]
        for pos, i in enumerate(self.target_instances):
            setattr(i, dname, getattr(i, dname) + values[pos])

    def fast_set_values(self, values):
        """store values without further checks"""
        assert self.can_be_target, "cannot serve as target"
        # broadcast values if necessary:
        values = self._broadcast(values)
        name = self.name_sequence[-1]
        for pos, i in enumerate(self.target_instances):
            setattr(i, name, values[pos])


_cached_values = {}
_cached_iteration = None

sympy2numpy = {
               sp.acos: np.arccos,
               sp.acosh: np.arccosh,
               sp.asin: np.arcsin,
               sp.asinh: np.arcsinh,
               sp.atan: np.arctan,
               sp.atan2: np.arctan2,
               sp.atanh: np.arctanh,
               sp.cos: np.cos,
               sp.cosh: np.cosh,
               sp.exp: np.exp,
               sp.log: np.log,
               sp.sin: np.sin,
               sp.sinh: np.sin,
               sp.sqrt: np.sqrt,
               sp.tan: np.tan,
               sp.tanh: np.tanh,
               }

#@profile
def eval(expr, instances, iteration=None):
    try:
        # if still up to date, return vals from cache:
        if iteration is not None and _cached_iteration == iteration:
            print("(used the cache)")
            return _cached_values[expr]
    except:
        pass
    t = type(expr)
    # else compute them anew:
    if t == D.Variable:
        vals = np.array(expr.eval(instances))
    elif t == _DotConstruct:
        vals = expr.eval(instances)
    elif t == sp.Add:
        vals = np.sum([eval(a, instances) for a in expr.args], axis=0)
    elif t == sp.Mul:
        vals = np.prod([eval(a, instances) for a in expr.args], axis=0)
    elif t == sp.Pow:
        vals = eval(expr.args[0], instances) ** eval(expr.args[1], instances)
        vals[np.where(np.isnan(vals))] = 0
    elif type(t) == sp.FunctionClass and t.nargs == {1}:
        # it is a unary sympy function
        vals = sympy2numpy[t](expr.args[0])
    # TODO: other types of expressions, including function evaluations!
    else:
        # simple scalar for broadcasting:
        vals = np.array([float(expr)])
    try:
        # store vals in cache:
        _cached_values[expr] = vals
        _cached_iteration = iteration
    except:
        pass
    return vals
