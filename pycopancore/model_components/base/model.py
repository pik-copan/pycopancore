"""base component's Model component mixin class plus essential framework logics 

This class is the Model component mixin of the base model component and also owns the configure
method. This method is central to the framework since it fuses together
the used classes and puts information about process types and variables
in special list to be accessed by the runner.
"""

# TODO: for clarity, move framework logics into separate class this class inherits from

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .model_logics import ModelLogics # only in base component
from pycopancore.model_components import abstract
from . import interface as I
from . import World, Cell, Nature, Individual, Culture, Society, \
    Metabolism

#
#  Define class Model
#


class Model (ModelLogics, I.Model, abstract.Model):
    """base model component mixin class.

    This is the base.model file. It serves two purposes:
    1. Be a the model class of the base component, providing the information
    about which mixins are to be used of the component AND:
    2. Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    #
    # Definitions of class attributes
    #

    entity_types = [World, Cell, Individual, Society]
    process_taxa = [Nature, Culture, Metabolism]

    #
    #  Definitions of internal methods
    #

    __configured = False

    def __new__(cls, *args, reconfigure=False, **kwargs):
        """Perform __new__ method.

        Only when an instance of Model is created for the first time the
        method configure is called.
        """
        # reconfigure = kwargs['reconfigure']
        # reconfigure = kwargs.get('reconfigure', False)
        if not cls.__configured or reconfigure:
            ModelLogics.configure(cls)
        return super(Model, cls).__new__(cls)

    def __init__(self,
                 **kwargs
                 ):
        """Initialize an instance of Model.

        Parameters
        ----------
        kwargs: Not in Use right now
        """
        super().__init__(**kwargs)

        self._process_taxon_objects = {pt: pt() for pt in self.process_taxa}
        self.entities_dict = {}
        for c in self.entity_types:
            self.entities_dict[c] = c.instances

        # TODO:
        # is it necessary to make all items in self.entities_dict known
        # to the object itself?

        # TODO:
        # Is this really what owning_classes is about???
        # Tell all variables and proceses which entities they have,
        # so set v/p.owning_classes:
        # for (p, oc) in self.processes:
        #     p.owning_classes = self.entities_dict[oc]
        # for (v, oc) in self.variables:
        #     v.owning_classes = self.entities_dict[oc]

        print('     base model instantiated')

    def __repr__(self):
        """Return a string representation of the base.Model."""
        # Is it necessary to list all objects? Or are classes sufficient?
        keys_entities = []
        keys_process_taxa = []
        for key, item in self.entities_dict:
            keys_entities.append(key)
        for key, item in self._process_taxon_objects:
            keys_process_taxa.append(key)
        return (super().__repr__() +
                ('base.model object with entities {} /'
                 'and process taxa {}'.format(keys_entities, keys_process_taxa)
                 )
                )
