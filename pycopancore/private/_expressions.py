"""Created on Mar 20, 2017.

@author: heitzig
"""

# defines logics to deal with symbolic expressions and their evaluation

import random
import numpy as np
import sympy as sp
import scipy.special

from .. import data_model as D
from .. import private

from numba import jit, njit

import inspect
from profilehooks import coverage, profile


class _Unknown(object):
    def __str__(self):
        return "unknown"


unknown = _Unknown()

# hierarchical aggregation functions:


def aggregation(npfunc):

    @njit
    def func(values, lens):
        # values = np.array(values)
        results = np.zeros(len(lens), dtype=values.dtype)
        offset = 0
        for i in range(len(lens)):
            newoffset = offset + lens[i]
            results[i] = npfunc(values[offset:newoffset])
            offset = newoffset
        return list(results)

    return func


name2numpy = {
    "all": np.all,
    "any": np.any,
    "max": np.max,
    "mean": np.mean,
    "median": np.median,
    "min": np.min,
    "std": np.std,
    "sum": np.sum,
    "var": np.var,
}
aggregation_names = set(name2numpy.keys())
name2aggregation = {name: aggregation(func)
                    for name, func in name2numpy.items()}


# hierarchical broadcasting:

@njit
def _broadcast(values, lens):
    result = np.zeros(np.sum(np.array(lens)))
    offset = 0
    for i, l in enumerate(lens):
        newoffset = offset + l
        result[offset:newoffset] = values[i]
        offset = newoffset
    return result


def broadcast(values, layout):
    for lens in layout:
        values = _broadcast(values, lens)
    return values


def layout2lens(layout):
    result = layout[-1]
    for lens in reversed(layout[:-1]):
        offset = 0
        newresult = []
        for i, l in enumerate(lens):
            newoffset = offset + l
            newresult.append(sum(result[offset:newoffset]))
            offset = newoffset
        result = newresult
    return result


def get_cardinalities_and_branchings(expr):
    try:
        return expr.cardinalities, expr.branchings
    except:
        # use longest cardinalities of args:
        cbs = [get_cardinalities_and_branchings(arg)
               for arg in expr.args]
        if len(cbs) == 0:
            return [1], []
        return cbs[np.argmax([len(c[0]) for c in cbs])]


class _DotConstruct (sp.AtomicExpr):
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

    _initialized = None
    """whether it was initialized already"""

    # needed to make sympy happy:
    _argset = ()
    args = ()
    is_Add = False
    is_float = False
#    is_symbol = True
#    is_Symbol = True
    precedence = sp.printing.precedence.PRECEDENCE["Atom"]

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
        if isinstance(owning_class_or_var, D.Variable) \
                or name_sequence[0] in aggregation_names:
            uid = repr(owning_class_or_var) \
                + str(name_sequence) + str(arg)
        else:
            uid = repr(getattr(owning_class_or_var, name_sequence[0])) \
                + str([None] + name_sequence[1:]) + str(arg)
        return super().__new__(cls,
                               uid,
                               **assumptions)

    def __init__(self,
                 owning_class_or_var,
                 name_sequence,
                 arg=None
                 ):
        super().__init__()

        if self._initialized is None:
            self._initialized = True

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
        if self.arg is not None:
            # append name to argument:
            return _DotConstruct(self._owning_class_or_var,
                                 self.name_sequence,
                                 arg=getattr(self.arg, name))
        elif self.name_sequence[-1] in aggregation_names:
            # add an argument:
            arg = _DotConstruct(self._owning_class_or_var,
                                self.name_sequence[:-1] + [name])
            return _DotConstruct(self._owning_class_or_var,
                                 self.name_sequence,
                                 arg=arg)
        else:
            # append name to name_sequence:
            return _DotConstruct(self._owning_class_or_var,
                                 self.name_sequence + [name])
        # Note that this causes hasattr(...) to always return True!
        # Hoping this causes no problem...

    def __call__(self, *args, **kwargs):
        assert self.arg is None, "can't have a ( behind a ) here"
        if self.name_sequence[-1] in aggregation_names:
            return _DotConstruct(self._owning_class_or_var,
                                 self.name_sequence,
                                 arg=args[0])
        else:
            return sp.AtomicExpr()

    def __repr__(self):
        repr = self.owning_class.__name__ + "." + ".".join(self.name_sequence)
        if self.arg is not None:
            repr += "(" + str(self.arg) + ")"
        return repr

    def __str__(self):
        return self.__repr__()

    # needed to make sympy happy: (may need further later)
    def _sympystr(self, *args, **kwargs):
        return self.__repr__()

    def match(self, *args, **kwargs):
        return None

    def is_constant(self, *args, **kwargs):
        return False

    def _eval_expand_mul(self, *args, **kwargs):
        return self

    def _eval_Eq(self, *args, **kwargs):
        return None

# this does not work unfortunately:
#    def __eq__(self, other):
#        print("eq?")
#        if self._target_instances is private.unknown:
#            print("std.")
#            return sp.AtomicExpr.__eq__(self, other)
#        else:
#            print("Eq")
#            return sp.Eq(self, other)
# so A == B cannot be used in formulas, instead sp.Eq(A,B) must be used.

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
        elif not issubclass(self._owning_class_or_var,
                            private._AbstractEntityMixin):
            # replace interface class by composite class, by using
            # owning_class of any Variable attribute of interface class:
            self._owning_class_or_var = \
                [v for v in self._owning_class_or_var.__dict__.values()
                 if isinstance(v, D.Variable)][0].owning_class
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
        # print("      (analysing instance structure of",self,")")
        oc = self.owning_class
        items = oc.instances
        branchings = [[len(items)]]
        cardinalities = [1, len(items)]  # store initial cardinality
        for name in self.name_sequence[:-1]:
            if name in aggregation_names:
                break
            # each item is a set of instances:
            if hasattr(items[0], "__iter__"):
                branchings.append([len(instance_set)
                                   for instance_set in items])
                items = [getattr(i, name)
                         for instance_set in items
                         for i in instance_set]
                # store cardinality after the branching:
                cardinalities.append(len(items))
            else:
                items = [getattr(i, name) for i in items]
                # items may now be a list of instances or a list of sets of
                # instances...
        if hasattr(items[0], "__iter__"):
            branchings.append([len(instance_set)
                               for instance_set in items])
            items = [i
                     for instance_set in items
                     for i in instance_set]
            # store cardinality after the branching:
            cardinalities.append(len(items))
        self._target_instances = items
        self._branchings = branchings
        self._cardinalities = cardinalities

    def eval(self, instances=None):
        """gets referenced attribute values and performs aggregations
        where necessary.
        """
        self.owning_class  # to make sure it and name_sequence are defined...
        items = self.owning_class.instances if instances is None else instances
        for pos, name in enumerate(self.name_sequence):
            if name in aggregation_names:
                # make sure items is list of instances not list of sets:
                if hasattr(items[0], "__iter__"):
                    items = [i
                             for instance_set in items
                             for i in instance_set]
                # TODO:
                # construct arg from name_sequence if None
                if self.arg is None:
                    arg_name_sequence = self.name_sequence[:pos] \
                        + self.name_sequence[pos + 1:]
                    self.arg = _DotConstruct(self.owning_class,
                                             arg_name_sequence)
                # sic! (not items!):
                arg_values = list(eval(self.arg, instances))
                cardinalities, branchings = \
                    get_cardinalities_and_branchings(self.arg)
                aggregation_level = cardinalities.index(len(items))
                layout = branchings[aggregation_level:] \
                    if aggregation_level < len(cardinalities) - 1 \
                    else [[1 for i in items]]
                lens = layout2lens(layout)
                return name2aggregation[name](arg_values, lens)
            # each value is a set of instances:
            if hasattr(items[0], "__iter__"):
                items = [getattr(i, name)
                         for instance_set in items
                         for i in instance_set]
            else:
                items = [getattr(i, name) for i in items]
        return items

    def _broadcast(self, values):
        """broadcast a list of values from entities at an intermediate level
        to their "offspring" entities at the final level"""
        value_level = self.cardinalities.index(len(values))
        if value_level < len(self.cardinalities) - 1:
            values = broadcast(values, self.branchings[value_level:])
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

#    def __iter__(self):
#        print("AHA!")
#        yield self

    def _eval_expand_power_base(self, **kwargs):
        return self


_cached_values = {}
_cached_iteration = None

func2numpy = {
    sp.Abs: np.abs,
    sp.acos: np.arccos,
    sp.acosh: np.arccosh,
    sp.asin: np.arcsin,
    sp.asinh: np.arcsinh,
    sp.atan: np.arctan,
    sp.atan2: np.arctan2,
    sp.atanh: np.arctanh,
    sp.ceiling: np.ceil,
    sp.cos: np.cos,
    sp.cosh: np.cosh,
    sp.erf: scipy.special.erf,
    sp.erfc: scipy.special.erfc,
    sp.erfinv: scipy.special.erfinv,
    sp.erfcinv: scipy.special.erfcinv,
    sp.exp: np.exp,
    sp.floor: np.floor,
    sp.Heaviside: lambda x: 1 - (x < 0).astype(int),
    sp.log: np.log,
    sp.sin: np.sin,
    sp.sinh: np.sin,
    sp.sqrt: np.sqrt,
    sp.tan: np.tan,
    sp.tanh: np.tanh,
}
binary2numpy = {
    sp.Eq: np.equal,
    sp.Ge: np.greater_equal,
    sp.Gt: np.greater,
    sp.Le: np.less_equal,
    sp.Lt: np.less,
    sp.Ne: np.not_equal,
}
nary2numpy = {
    sp.Add: np.sum,
    sp.And: np.logical_and,
    sp.Mul: np.prod,
    sp.Or: np.logical_or,
    sp.Xor: np.logical_xor,
}

# @profile


def _eval(expr, iteration=None):
    try:
        # if still up to date, return vals from cache:
        if iteration is not None and _cached_iteration == iteration:
            print("(used the cache)")
            return _cached_values[expr]
    except:
        pass
    t = type(expr)
    tt = type(t)
    if (isinstance(expr, sp.Expr) or tt == sp.FunctionClass) \
            and len(expr.args) > 0:
        args = expr.args
        argvals = [None for a in args]
        argcards = [None for a in args]
        argbrs = [None for a in args]
        for i, arg in enumerate(args):
            argvals[i], argcards[i], argbrs[i] = \
                _eval(arg, iteration=iteration)
        # TODO: broadcast shorter args to level of longest arg!
        longest = np.argmax([len(c) for c in argcards])
        cardinalities = argcards[longest]
        branchings = argbrs[longest]
        for i, arg in enumerate(args):
            if i != longest:
                l = argvals[i].size
                pos = 0 if l == 1 else cardinalities.index(l)
                argvals[i] = broadcast(argvals[i], branchings[pos:])
    if t in (D.Variable, _DotConstruct):
        vals = np.array(expr.eval())
        cardinalities = expr.cardinalities
        branchings = expr.branchings
    elif t == sp.Not:
        vals = np.logical_not(argvals)
    # binary operators:
    elif t in binary2numpy:
        vals = binary2numpy[t](argvals[0], argvals[1])
    # ternary operators:
    elif t == sp.ITE:
        truthvals = argvals[0]
        trues = list(np.where(truthvals == True)[0])
        vals = argvals[2]
        vals[trues] = argvals[1][trues]
    # n-ary operators:
    elif t in nary2numpy:
        vals = nary2numpy[t](argvals, axis=0)
    # Following: = True if even no. of arguments is True = Not(Xor):
    elif t == sp.Equivalent:
        vals = np.logical_not(np.logical_xor(argvals, axis=0))
    elif t == sp.Nand:
        vals = np.logical_not(np.logical_and(argvals, axis=0))
    elif t == sp.Nor:
        vals = np.logical_not(np.logical_or(argvals, axis=0))
    elif t == sp.Pow:
        base = argvals[0]
        exponent = argvals[1]
        # FIXME: do the following much better!
#        EPS = 1e-10
#        LARGE = 1e50
#        base[np.where(np.isnan(base))] = 0
#        # try to avoid overflows due to (small abs)**(negative):
#        base[np.where(np.logical_and(np.abs(base) < EPS, exponent < 0))] = EPS
#        # try to avoid overflows due to (large abs)**(positive):
#        base[np.where(np.logical_and(
#             np.abs(base) > LARGE, exponent > 0))] = LARGE
#        # try to avoid invalid values due to (negative)**(non-integer):
#        base[np.where(np.logical_and(base < 0, exponent % 1 != 0))] = EPS
#        print(base[:10],exponent[:10])
        vals = base ** exponent
        vals[np.where(np.isnan(vals))] = 0  # FIXME: is this a good idea?
    # TODO: other types of expressions, including function evaluations!
    # other functions/unary operators:
    elif tt == sp.FunctionClass:
        # it is a unary (?) sympy function
        vals = func2numpy[t](argvals[0])
    else:
        # simple scalar for broadcasting:
        # clumsy way of converting sympy True to normal True:
        if expr is True:
            expr = True
        elif expr == False:
            expr = False
        else:
            expr = float(expr)
        vals = np.array([expr])
        cardinalities = [1]
        branchings = []
    try:
        # store vals in cache:
        _cached_values[expr] = (vals, cardinalities, branchings)
        _cached_iteration = iteration
#        print("(stored in cache)")
    except:
        pass
    return vals, cardinalities, branchings


def eval(expr, iteration=None):
    vals, cardinalities, branchings = _eval(expr)
    return vals
