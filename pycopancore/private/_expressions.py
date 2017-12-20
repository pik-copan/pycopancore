"""Created on Mar 20, 2017.

@author: heitzig
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# defines logics to deal with symbolic expressions and their evaluation

import numpy as np
import sympy as sp
import scipy.special

from .. import data_model as D
from .. import private

from numba import njit


class _Unknown(object):
    def __str__(self):
        return "unknown"
    def update(self, *args):
        return self

unknown = _Unknown()

class _Unset(object):
    def __str__(self):
        return "unset"
    def update(self, *args):
        return self

unset = _Unset()


# hierarchical aggregation functions:

def aggregation(npfunc):
    """Dummy docstring"""

    # TODO: add docstring to function

    @njit
    def func(values, lens):
        """Dummy docstring"""

        # TODO: add docstring to function
        # values = np.array(values)
        results = np.zeros(len(lens), dtype=values.dtype)
        offset = 0
        for i, le in enumerate(lens):
            newoffset = offset + le
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
    """Dummy docstring"""
    # TODO: add docstring to function
    result = np.zeros(np.sum(np.array(lens)))
    offset = 0
    for i, le in enumerate(lens):
        newoffset = offset + le
        result[offset:newoffset] = values[i]
        offset = newoffset
    return result


def broadcast(values, layout):
    """Dummy docstring"""
    # TODO: add docstring to function
    for lens in layout:
        values = _broadcast(values, lens)
    return values


def layout2lens(layout):
    """Dummy docstring"""
    # TODO: add docstring to function
    result = layout[-1]
    for lens in reversed(layout[:-1]):
        offset = 0
        newresult = []
        for le in lens:
            newoffset = offset + le
            newresult.append(sum(result[offset:newoffset]))
            offset = newoffset
        result = newresult
    return result


def get_cardinalities_and_branchings(expr):
    """Dummy docstring"""
    # TODO: add docstring to function
    try:
        return expr.cardinalities, expr.branchings
    except BaseException:
        # use longest cardinalities of args:
        cbs = [get_cardinalities_and_branchings(arg)
               for arg in expr.args]
        if len(cbs) == 0:
            return [1], []
        return cbs[np.argmax([len(c[0]) for c in cbs])]


class _DotConstruct(sp.AtomicExpr):
    """A _DotConstruct represents a syntactical construct with dots,
    starting with an entity-type or process taxon class,
    followed by zero or more ReferenceVariables or SetVariables
    or aggregation keywords such as sum, and ending in either an attribute,
    e.g. SocialSystem.sum.cells.population
    or an aggregation keyword without evaluation,
    e.g. SocialSystem.world.sum,
    or an aggregation keyword with evaluation,
    e.g. SocialSystem.world.sum(some expression).
    """

    _start = None
    """the entity-type, process taxon, ReferenceVariable or SetVariable 
    at the start of the dot construct, e.g. SocialSystem or Environment.cells"""
    _attribute_sequence = None
    """the sequence of further names, which must be codenames of variables,
    e.g. ["cells","population"]"""
    _aggregation = None
    """the optional name of an aggregation function 
    at the end of the construct, e.g., "sum"."""
    _argument = None
    """the optional argument expression of the aggregation function, e.g.
    SocialSystem.world.sum.cells.population * SocialSystem.world.sum.cells.capital"""
    _can_be_target = None
    """whether this can be a target (i.e., does not involve aggregation)"""

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
    _iterable = False

    # needed to make sphinx happy:
    __qualname__ = "pycopancore.private._expressions._DotConstruct"


    # inheritance from Symbol is a little tricky since Symbol has a custom
    # __new__ method that returns the same object everytime the name is the
    # same! We break this behaviour by using random Symbol.names so that we
    # can multiple copies of a Variable having the same name, to be attached
    # to different entity types:
    @staticmethod
    def __new__(cls,
                start,
                attribute_sequence,
                *args,
                aggregation=None,
                argument=None,
                **assumptions):

        uid = str(start)  # repr

        if len(attribute_sequence) > 0:
            uid += "." + ".".join(attribute_sequence)
        if aggregation:
            uid += "." + aggregation
            if argument:
                uid += "(" + str(argument) + ")"  # repr
#        print("_DotConstruct.__new__ with uid", uid)
        return super().__new__(cls, uid, **assumptions)

    def __init__(self,
                 start,
                 attribute_sequence,
                 aggregation=None,
                 argument=None
                ):
        super().__init__()

        if self._initialized is None:
            self._initialized = True

            self._start = start
            self._attribute_sequence = attribute_sequence
            self._aggregation = aggregation
            self._argument = argument

            self._can_be_target = (aggregation is None)

            self._target_class = unknown
            self._target_variable = unknown
            self._target_instances = unknown
            self._branchings = unknown
            self._cardinalities = unknown

#            print("_DotConstruct.__init__ of",self,"performed")
        else:
#            print("repeated _DotConstruct.__init__ of",self,"skipped")
            pass

    def __getattr__(self, name):
        """accessing an attribute of a _DotConstruct basically
        returns a new _DotConstruct that is extended by the name of this
        attribute, giving special treatment to aggregations"""
        if name == "__qualname__":  # needed to make sphinx happy
            return "DUMMY"  # FIXME!
#        print("_DotConstruct.__getattr__(", self, ",", name, ")")
        if self._argument is not None:  # we are an aggregation with argument
            # append name to argument:
#            print("extending argument",self._argument,"by",name)
            newarg = getattr(self._argument, name)
            newdc = _DotConstruct(self._start,
                                  self._attribute_sequence,
                                  aggregation=self._aggregation,
                                  argument=newarg)
        elif self._aggregation:  # we are an aggregation without argument yet
            # add an argument:
            argument = _DotConstruct(self._start,
                                self._attribute_sequence + [name])
#            print("adding argument",argument,"to aggregation of type",self._aggregation)
            newdc = _DotConstruct(self._start,
                                  self._attribute_sequence,
                                  aggregation=self._aggregation,
                                  argument=argument)
        elif name in aggregation_names:  # we become an aggregation
#            print("adding aggregation of type",name)
            newdc = _DotConstruct(self._start,
                                  self._attribute_sequence,
                                  aggregation=name)
        else:  # append name to attribute_sequence:
#            print("adding variable reference named",name)
            newdc = _DotConstruct(self._start,
                                  self._attribute_sequence + [name])
        return newdc
        # Note that this causes hasattr(...) to always return True!
        # Hoping this causes no problem...

    def __call__(self, *args, **kwargs):
        """calling is only allowed if we are an aggregation without argument yet,
        and results in adding an argument"""
        # TODO: reactivate the following line after fixing sphinx bug:
#        assert self._aggregation and not self._argument, "can't have brackets here"
        assert len(args) == 1, "must have exactly one argument"
        return _DotConstruct(self._start,
                             self._attribute_sequence,
                             aggregation=self._aggregation,
                             argument=args[0])
# TODO: understand why an earlier version had this:
#        else:
#            return sp.AtomicExpr()

    def __repr__(self):
        r = repr(self._start)
        if len(self._attribute_sequence) > 0:
            r += "." + ".".join(self._attribute_sequence)
        if self._aggregation:
            r += "." + self._aggregation
            if self._argument:
                r += "(" + repr(self._argument) + ")"
        return r

    def __str__(self):
#        return self.__repr__()
        r = str(self._start)
        if len(self._attribute_sequence) > 0:
            r += "." + ".".join(self._attribute_sequence)
        if self._aggregation:
            r += "." + self._aggregation
            if self._argument:
                r += "(" + str(self._argument) + ")"
        return r

    # needed to make sympy happy: (may need further later)
    def _sympystr(self, *args, **kwargs):
        return self.__str__()

    def match(self, *args, **kwargs):
        return None

    def is_constant(self, *args, **kwargs):
        return False

    def _eval_expand_mul(self, *args, **kwargs):
        return self

    @staticmethod
    def _eval_Eq(*args, **kwargs):
        return None

# this does not work unfortunately:
#    def __eq__(self, other):
#        print("eq?")
#        if self._target_instances is unknown:
#            print("std.")
#            return sp.AtomicExpr.__eq__(self, other)
#        else:
#            print("Eq")
#            return sp.Eq(self, other)
# so A == B cannot be used in formulas, instead sp.Eq(A,B) must be used.

    # TODO: put a leading underscore before as many method names as possible
    # (only not those needed by sympy), to avoid name clashes with variables

    @property  # read-only
    def owning_class(self):
        """return the class owning the _DotConstruct"""
        if isinstance(self._start, D.Variable):
            return self._start.owning_class
        elif self._start._composed_class:
            return self._start._composed_class
        else:
            return self._start

    @property  # read-only
    def target_class(self):
        """return the class owning the target attribute"""
        assert self._can_be_target, "cannot serve as target"
        if self._target_class is unknown:
            if isinstance(self._start, (D.ReferenceVariable, D.SetVariable)):
                cls = self._start.type  # referred entity type/taxon
            else:
                cls = self._start
            for name in self._attribute_sequence[:-1]:
                var = getattr(cls, name)
                assert isinstance(var, (D.ReferenceVariable, D.SetVariable))
                cls = var.type
            self._target_class = cls
#            print("finding target class of",self,"as",cls)
        return self._target_class

    @property  # read-only
    def target_variable(self):
        """return the Variable object representing the target attribute"""
        assert self._can_be_target, "cannot serve as target"
        if self._target_variable is unknown:
            self._target_variable = getattr(self.target_class,
                                            self._attribute_sequence[-1])
#            print("getting target variable of",self,"as",self._target_variable)
        return self._target_variable

    @property  # read-only
    def target_instances(self):
        """return the list of instances owning the referenced attributes,
        may contain instances more than once due to broadcasting"""
        assert self._can_be_target, "cannot serve as target"
        if self._target_instances is unknown:
            self._analyse_instances()
        return self._target_instances

    @property  # read-only
    def branchings(self):
        """return the list of branching lens at SetReferences,
        to be used in aggregation and broadcasting"""
        if self._target_instances is unknown:
            self._analyse_instances()
        return self._branchings

    @property  # read-only
    def cardinalities(self):
        """return the list of level cardinalities at SetReferences,
        to be used in aggregation and broadcasting"""
        if self._target_instances is unknown:
            self._analyse_instances()
        return self._cardinalities

    def _analyse_instances(self):
        # print("      (analysing instance structure of",self,")")
        oc = self.owning_class
        items = oc.instances
        branchings = [[len(items)]]
        cardinalities = [1, len(items)]  # store initial cardinality
        if isinstance(self._start, D.Variable):
            items = [getattr(i, self._start.codename) for i in items]
        for name in self._attribute_sequence[:-1]:
            # each item is a set of instances:
            if len(items) > 0 and hasattr(items[0], "__iter__"):
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
        if len(items) > 0 and hasattr(items[0], "__iter__"):
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

    # TODO add a method that differentiates symbolically w.r.t. some variable?

    def eval(self, instances=None):
        """gets referenced attribute values and performs aggregations
        where necessary.
        """
#        print("eval",self)
        try:
            items = self.owning_class.instances if instances is None else instances
        except:
            print(self)
            raise Exception
        if isinstance(self._start, D.Variable):
            items = [getattr(i, self._start.codename) for i in items]
        for pos, name in enumerate(self._attribute_sequence):
            if len(items) > 0 and hasattr(items[0], "__iter__"):
                items = [getattr(i, name)
                         for instance_set in items
                         for i in instance_set]
            else:
                items = [getattr(i, name) for i in items]
        if self._aggregation:
            assert self._argument is not None, "aggregation without argument"
            # make sure items is list of instances not list of sets:
            if len(items) > 0 and hasattr(items[0], "__iter__"):
                items = [i
                         for instance_set in items
                         for i in instance_set]
            # sic! (not items!):
            arg_values = eval(self._argument, instances)
            cardinalities, branchings = \
                get_cardinalities_and_branchings(self._argument)
            aggregation_level = cardinalities.index(len(items))
            layout = branchings[aggregation_level:] \
                if aggregation_level < len(cardinalities) - 1 \
                else [[1 for i in items]]
            lens = layout2lens(layout)
            items = name2aggregation[self._aggregation](arg_values, lens) \
                        if len(arg_values) > 0 else [0 for l in lens]
#            print("aggregation",self,items)
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
        assert self._can_be_target, "cannot serve as target"
        # broadcast values if necessary:
        values = self._broadcast(values)
        name = self._attribute_sequence[-1]
        for pos, i in enumerate(self.target_instances):
            setattr(i, name, getattr(i, name) + values[pos])

    def add_derivatives(self, values):
        """adds summands to referenced attribute values"""
        assert self._can_be_target, "cannot serve as target"
        # broadcast values if necessary:
        values = self._broadcast(values)
        dname = "d_" + self._attribute_sequence[-1]
        for pos, i in enumerate(self.target_instances):
            setattr(i, dname, getattr(i, dname) + values[pos])

    def fast_set_values(self, values):
        """store values without further checks"""
        assert self._can_be_target, "cannot serve as target"
        # broadcast values if necessary:
        values = self._broadcast(values)
        name = self._attribute_sequence[-1]
        for pos, i in enumerate(self.target_instances):
            setattr(i, name, values[pos])

#    def __iter__(self):
#        print("AHA!")
#        yield self

    def _eval_expand_power_base(self, **kwargs):
        return self


func2numpy = {
    # unary:
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
    # n-ary:
    sp.Max: np.maximum,
    sp.Min: np.minimum,
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

_cached_values = {}
_cached_iteration = None

have_warned = False

# TODO: use a separate cache for expressions that do not change during ode
# integration and devaluate it only between integration intervals.
# TODO: also use sympy to simplify and maybe even solve systems of equations
def _eval(expr, iteration=None):
    if iteration is not None:
        global _cached_iteration, _cached_values
        if _cached_iteration == iteration:
            # still up to date, so try returning vals from cache:
            try:
                res = _cached_values[expr]
#                print("read from cache:",expr)
                return res
            except KeyError:
                pass
        else:
            # clear cache:
            _cached_values = {}
            _cached_iteration = iteration
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
                length = argvals[i].size
                pos = 0 if length == 1 else cardinalities.index(length)
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
        trues = list(np.where(truthvals == True)[0])  # "==" is correct here, since it may be a sympy.True!! Do not replace "==" by "is"!!
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
        try:
            pass
#            base[np.where((base == 0)*(exponent < 0))] = 1e-10
        except:
            print("oops! couldn't set values")
        vals = base ** exponent
        isn = np.isnan(vals.astype("float"))
        if np.any(isn):
            wh = np.where(isn)[0]
            global have_warned
            if not have_warned:
                have_warned = True
                print("Warning: invalid value encountered in power\nbase:",
                      args[0], "=", base[wh], "\nexponent:", args[1], "=", exponent[wh])
            vals[wh] = 0  # TODO: is this a good idea?
    # TODO: other types of expressions, including function evaluations!
    # other functions/unary operators:
    elif tt == sp.FunctionClass:
        # it is a sympy function
        vals = func2numpy[t](*argvals)
    else:
        # simple scalar for broadcasting:
        # clumsy way of converting sympy True to normal True:
        if expr is True:
            expr = True
        elif expr is False:
            expr = False
        else:
            expr = float(expr)
        vals = np.array([expr])
        cardinalities = [1]
        branchings = []
    if iteration is not None:
        # store vals in cache:
        _cached_values[expr] = (vals, cardinalities, branchings)
#        print("stored in cache:",expr)
    return vals, cardinalities, branchings


def eval(expr, iteration=None):
    """Dummy docstring - wrap private _eval function?"""
    # TODO: add docstring to function
    vals, cardinalities, branchings = _eval(expr, iteration=iteration)
    return vals


def get_vars(expr):
    """find all variables occurring in Expression"""
    if isinstance(expr, (D.Variable, _DotConstruct)):
        if expr._can_be_target:
            return set([expr.target_variable])
        return get_vars(expr._argument)
    varset = set()
    for a in expr.args:
        varset.update(get_vars(a))
    return varset
