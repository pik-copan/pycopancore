'''
Created on Mar 20, 2017

@author: heitzig
'''

# defines logics to deal with symbolic expressions and their evaluation

import random
import numpy as np
import sympy as sp

from .. import data_model


class _AttributeReference (sp.Symbol):
    """An AttributeReference represents a syntactical construct with dots, e.g.
    I.Cell.world.nature.atmospheric_carbon"""

    reference_variable = None
    """the ReferenceVariable at the start of the attribute reference, 
    e.g. I.Cell.world"""
    name_sequence = None
    """the sequence of further attribute names,
    e.g. ["nature","atmospheric_carbon"]"""

    # inheritance from Symbol is a little tricky since Symbol has a custom
    # __new__ method that returns the same object everytime the name is the
    # same! We break this behaviour by using random Symbol.names so that we
    # can multiple copies of a Variable having the same name, to be attached
    # to different entity types:
    @staticmethod
    def __new__(cls, reference_variable, name_sequence, *args, **assumptions):
        return super().__new__(cls,
                               str(random.random()),
                               **assumptions)

    def __init__(self, reference_variable, name_sequence):
        self.reference_variable = reference_variable
        self.name_sequence = name_sequence

    def __getattr__(self, name):
        """return an object representing an attribute of this attribute"""
        return _AttributeReference(self.reference_variable,
                                   self.name_sequence + [name])

    _target_class = None
    def get_target_class(self):
        """return the class owning the referenced attribute"""
        if self._target_class is None:
            instance = self.reference_variable.get_value(
                            self.reference_variable.owning_class.instances[0])
            if type(instance) == set:
                instance = next(iter(instance))
            for name in self.name_sequence[:-1]:
                instance = getattr(instance, name)
                if type(instance) == set:
                    instance = next(iter(instance))
            self._target_class = instance.__class__
        return self._target_class

    def get_target_variable(self):
        """return the Variable object of the referenced attribute"""
        return getattr(self.get_target_class(), self.name_sequence[-1])

    def get_target_instances(self, instances):
        """gets the instances owning the referenced attributes"""
        items = self.reference_variable.get_values(instances)
        for name in self.name_sequence[:-1]:
            items = [getattr(i, name) for i in items]
        return items

    def get_values(self, instances):
        """gets referenced attribute values"""
        items = self.reference_variable.get_values(instances)
        for name in self.name_sequence:
            items = [getattr(i, name) for i in items]
        return items

    def add_values(self, instances, values):
        """adds summands to referenced attribute values"""
        items = self.reference_variable.get_values(instances)
        for name in self.name_sequence[:-1]:
            items = [getattr(i, name) for i in items]
        name = self.name_sequence[-1]
        for pos, i in enumerate(items):
            setattr(i, name, getattr(i, name) + values[pos])

    def add_derivatives(self, instances, values):
        """adds summands to referenced attribute values"""
        items = self.reference_variable.get_values(instances)
        for name in self.name_sequence[:-1]:
            items = [getattr(i, name) for i in items]
        dname = "d_"+self.name_sequence[-1]
        for pos, i in enumerate(items):
            setattr(i, dname, getattr(i, dname) + values[pos])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.reference_variable.owning_class) + str(self.reference_variable) + str(self.name_sequence)


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
    if t == data_model.Variable:
        vals = np.array(expr.get_values(instances))
    elif t == _AttributeReference:
        vals = expr.get_values(instances)
    elif t == sp.Add:
        vals = np.sum([eval(a, instances) for a in expr.args], axis=0)
    elif t == sp.Mul:
        vals = np.prod([eval(a, instances) for a in expr.args], axis=0)
    elif t == sp.Pow:
        vals = eval(expr.args[0], instances) ** eval(expr.args[1], instances)
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
