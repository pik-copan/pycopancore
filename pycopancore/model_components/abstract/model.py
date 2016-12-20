class Model(object):
    """
    Abstract class from which all model components must be derived
    """

    # class attributes later holding the specific model component's metadata:

    name = None  # a unique name for the model component
    description = None  # some description
    requires = None  # list of other model components required for this model
    # component to make sense

    # Lists of Mixin classes contributed by this component:

    entity_types = None
    process_taxa = None

    def __init__(self):
        return NotImplemented
