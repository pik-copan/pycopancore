from pycopancore.data_model import Variable
from networkx import DiGraph, Graph
from docutils.nodes import thead

# Social networks between individuals:

acquaintance_network = \
    Variable("acquaintance network",
             """Basic undirected social network of acquaintance between 
             Individuals. Most other social networks will be subgraphs of this.""",
             ref="https://en.wikipedia.org/wiki/Interpersonal_relationship#Stages",
             datatype=Graph)

friendship_network = \
    Variable("friendship/intimate/family network",
             """Smaller (and typically slower-changing) undirected network of 
             actual friendships and other intimate relationships such as close
             familiar ties etc. May have a significantly different structure,
             e.g. a qualitatively (less heavy-tailed) degree distribution
             and a higher transitivity.""",
             ref="https://en.wikipedia.org/wiki/Intimate_relationship",
             datatype=Graph)

trusted_business_network = \
    Variable("trusted business partners/colleagues network",
             """Similar undirected network for the business side of life, may
             overlap.
             Not meant to include all business contacts such as competitors,
             customers etc. which should rather be represented by a network
             between firms""",
             ref="https://en.wikipedia.org/wiki/Interpersonal_relationship#Types",
             datatype=Graph)

# Networks between firms and potentially also individuals and societies:

supply_chain_network = \
    Variable("supply chain network",
             """Directed network of actual (not potential) supplier-customer 
             relationships through the economic supply chain, including the
             final end customer link and potentially initial links from
             societies.""",
             ref="https://en.wikipedia.org/wiki/Supply_chain",
             datatype=DiGraph)

# Networks between firms only:

trusted_competitor_network = \
    Variable("trusted competitor network",
             """Undirected network of basic trust relationships between
             competiting firms, to be used in cartel formation model components.
             Represents the prerequisites of forming a cartel, not the actually
             formed cartel structure (which is rather a set of sets of firms).""",
             ref="https://en.wikipedia.org/wiki/Cartel",
             datatype=Graph)

# Networks and coalitions between societies only:

trusted_diplomatic_network = \
    Variable("trusted diplomatic network",
             """Undirected network of basic trust relationships between
             societies, to be used in (intersocietal) coalition formation model
             components. Represents the prerequisites of forming a coalition, 
             not the actually formed coalition structure (which is rather a set
             of sets of societies).""",
             ref="https://en.wikipedia.org/wiki/Coalition#International_relations",
             datatype=Graph)

intersocietal_coalition_structure = \
    Variable("intersocietal coalition structure",
             """(a set of sets of societies)""",
             datatype=set)

