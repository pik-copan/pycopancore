class ImitationPG (object):
    
    def __init__(self, network_var, trait_var, rate_var):
        """generate a group of processes that realize imitation of trait_var 
        in the network given by network_var"""
        
        def imitate(entity, unused_t):
            """perform an individual imitation event"""
            # select a random node from network:
            net = network_var.get_value(entity)
            i = random.choice(net.nodes())
            j = random.choice(net.neighbors(i))
            trait_var.set_value(i, trait_var.get_value(j))
            
        processes = [
            Event("imitation of " + str(trait_var) + " in network " + str(network_var),
                  [trait_var],
                  rate_var,
                  imitate)
            ]
        
        return processes

# in entity type implementation mixin class:
#  processes = [...] + ImitationPG(network_var=B.Metabolism.acquaintance_network,...)