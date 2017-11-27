"""Master data model for culture."""

from .. import Variable

from networkx import DiGraph, Graph

from .. import unity


class Culture:

    # Social networks between individuals:
    
    
    intimate_relationship_network = \
        Variable("intimate relationship network",
                 """Basic social network of intimate relationship between
                 Individuals. Could be used to form hauseholds.""",
                 ref="Brehm, S. S. (1992). The McGraw-Hill series in social psychology. Intimate relationships, 2nd ed. New York: Mcgraw-Hill Book Company.http://psycnet.apa.org/record/1991-98375-000 ",
                 scale='ordinal',
                 datatype=Graph) 
    
      
    
    
    acquaintance_network = \
        Variable("acquaintance network",
                 """Basic undirected social network of acquaintance between
                 Individuals. Most other social networks will be subgraphs of this.""",
                 ref="https://en.wikipedia.org/wiki/Interpersonal_relationship#Stages",
                 scale='nominal',
                 datatype=Graph)
    
    friendship_network = \
        Variable("friendship/intimate/family network",
                 """Smaller (and typically slower-changing) undirected network of
                 actual friendships and other intimate relationships such as close
                 familiar ties etc. May have a significantly different structure,
                 e.g. a qualitatively (less heavy-tailed) degree distribution
                 and a higher transitivity.""",
                 ref="https://en.wikipedia.org/wiki/Intimate_relationship",
                 scale='nominal',
                 datatype=Graph)
        
     political_preference_network = \
        Variable("political preference network",
                 """Larger (and typically slower-changing) undirected network of
                 political opinions and preferences etc. May be used to predict voting outcomes in democratic societies.""",
                 ref="https://doi.org/10.1017/S0003055404041413",
                 scale='nominal',
                 datatype=Graph)     
      
     knowledge_network = \
        Variable("knowledge network",
                 """Larger (and typically slower-changing) undirected network of
                 knowledge and information availability, etc. May be used to predict 
                 the consuption choices and entering business relationships.""",
                 ref="Hildreth and Kimble (2004). Knowledge Networks: Innovation Through Communities of Practice. London: Idea Group Publishing. https://books.google.de/books?hl=en&lr=&id=4ANHY1c6b6YC&oi=fnd&pg=PP1&dq=knowledge+networks&ots=8_8DPmfhO0&sig=t_OOtOH2vWtimzLW6S4YhKxK3iM#v=onepage&q=knowledge%20networks&f=false ",
                 scale='nominal',
                 datatype=Graph)  
    
    beliefs_network = \
        Variable("beliefs network",
                 """Larger (and typically slower-changing) undirected network of
                 beliefs, religion, etc. May be used to predict trust or ability to accept innovation, 
                 might influence consumer and buisness relationships.""",
                 ref="https://doi.org/10.1177/0951692898010004005",
                 scale='nominal',
                 datatype=Graph) 
    
    # TODO: maybe use "professional_network":
    trusted_business_network = \
        Variable("trusted business partners/colleagues network",
                 """Similar undirected network for the business side of life, may
                 overlap.
                 Not meant to include all business contacts such as competitors,
                 customers etc. which should rather be represented by a network
                 between firms""",
                 ref="https://en.wikipedia.org/wiki/Interpersonal_relationship#Types",
                 scale='nominal',
                 datatype=Graph)
    
    # Networks between firms and potentially also individuals and societies:
    # Link with metabolic profile
    
    supply_chain_network = \
        Variable("supply chain network",
                 """Directed network of actual (not potential) supplier-customer
                 relationships through the economic supply chain, including the
                 final end customer link and potentially initial links from
                 societies.""",
                 ref="https://en.wikipedia.org/wiki/Supply_chain",
                 scale='nominal',
                 datatype=DiGraph)
# Question: what is the difference between Graph and DiGraph and set as datatype? What is a different between direct and indirect network?  

  governance_network = \
        Variable("governance network",
                 """Directed network of power influence, including the manaement type 
                  and the of hierarchical relationships.""",
                 ref="https://www.elgaronline.com/view/9781840642254.00030.xml",
                 scale='ordinal',
                 datatype=DiGraph)
        
   alliance_network = \
        Variable("alliance network",
                 """Directed network of buisness or political agreement.""",
                 ref="https://doi.org/10.1177/0738894212443446; https://doi.org/10.1177/0022002700044002003",
                 scale='nominal',
                 datatype=DiGraph)     
    
        
    # Does it make sense to replace "firm" with "enterprise"? Enterprise is more general, could be either public or private.    
    
    # Networks between firms only:
    
    trusted_competitor_network = \
        Variable("trusted competitor network",
                 """Undirected network of basic trust relationships between
                 competiting firms, to be used in cartel formation model components.
                 Represents the prerequisites of forming a cartel, not the actually
                 formed cartel structure (which is rather a set of sets of firms).""",
                 ref="https://en.wikipedia.org/wiki/Cartel",
                 scale='nominal',
                 datatype=Graph)
        
   # What about metabolic profiles of firms / enterprises?
    
    # Networks and coalitions between societies only:
    
    trusted_diplomatic_network = \
        Variable("trusted diplomatic network",
                 """Undirected network of basic trust relationships between
                 societies, to be used in (intersocietal) coalition formation model
                 components. Represents the prerequisites of forming a coalition,
                 not the actually formed coalition structure (which is rather a set
                 of sets of societies).""",
                 ref="https://en.wikipedia.org/wiki/Coalition#International_relations",
                 scale='nominal',
                 datatype=Graph)
    
    intersocietal_coalition_structure = \
        Variable("intersocietal coalition structure",
                 """(a set of sets of societies)""",
                 scale='nominal',
                 datatype=set)
        
   # What about metabolic profile?
        
        
        
    # socio-cultural traits that may occur on different levels:
    
    is_environmentally_friendly = \
        Variable("is environmentally friendly",
                 """whether the entity is environmentally friendly or not""",
                 scale="ordinal", levels=[False, True], default=False)
        
        
        
   
    # How to represent institutions - rules of interaction? 
    # They could characterise network rules or entity attributes, or they could also form entities on their own
    # The following types of instituitions could be distinbuished: informal institutions and beliefs; formal and written institutions and codes of behavior; informal practise such as routines and convenstions.
    
