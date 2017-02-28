from ._abstract_entity_mixin import _AbstractEntityMixin
from .variable import Variable

class SetVariable(Variable):
    """
    set of other entities
    """
    
    entity_type = None
    """required entity type of referred entities"""
    
    def __init__(self, 
                 entity_type=_AbstractEntityMixin, 
                 **kwargs):
        super().__init__(**kwargs)
        self.entity_type = entity_type
        