'''
Created on Mar 20, 2017

@author: heitzig
'''

# defines logics to deal with symbolic expressions and their evaluation

import random
import numpy as np

from sympy import Symbol, Add, Mul, Pow

from .. import data_model


class _AttributeReference (Symbol):
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
    def __new__(cls, *args, **assumptions):
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

    def get_target_class(self, instance):
        """return the class owning the referenced attribute"""
        instance = self.reference_variable.get_value(instance)
        for name in self.name_sequence[:-1]:
            instance = getattr(instance, name)
        return instance.__class__

    def get_target_variable(self, instance):
        """return the Variable object of the referenced attribute"""
        return getattr(self.get_target_class(instance), self.name_sequence[-1])

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


def eval(expr, instances):
    if isinstance(expr, data_model.Variable):
        return np.array(expr.get_values(instances))
    t = type(expr)
    if t == Add:
        return np.sum([eval(a, instances) for a in expr.args], axis=0)
    if t == Mul:
        return np.prod([eval(a, instances) for a in expr.args], axis=0)
    if t == Pow:
        return expr.args[0] ** expr.args[1]
    if t == _AttributeReference:
        return expr.get_values(instances)
    # simple scalar for broadcasting:
    return np.array([float(expr)])
