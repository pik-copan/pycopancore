class Model(object):
    """
    Abstract class from which all model components must be derived
    """

    # class attributes later holding the specific model component's metadata:

    name = None  # a unique name for the model component
    description = None  # some description
    requires = []  # list of other model components required for this model
    # component to make sense

    # Mixin classes contributed by this component:
    individual_mixin = None
    cell_mixin = None
    society_mixin = None
    world_mixin = None

    culture_mixin = None
    nature_mixin = None
    metabolism_mixin = None

    def __init__(self):
        return NotImplemented
