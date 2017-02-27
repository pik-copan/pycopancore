from .variable import Variable

class ReferenceVariable(Variable):
    """
    reference to another entity or process taxon
    """
    
    type = None
    """required type of referred entity or taxon"""
    
    def __init__(self, 
                 type=object, 
                 **kwargs):
        super().__init__(**kwargs)
        self.type = type
        