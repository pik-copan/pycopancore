from ._abstract_entity_mixin import _AbstractEntityMixin
from .variable import Variable

class ReferenceVariable(Variable):
    """
    reference to another entity
    """
    
    entity_type = None
    """required entity type of referred entity"""
    
    def __init__(self, 
                 entity_type=_AbstractEntityMixin, 
                 **kwargs):
        super().__init__(**kwargs)
        self.entity_type = entity_type
        