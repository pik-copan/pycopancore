import json

#---configuration---

# seed
seed = 1

# runner
timeinterval = 10
timestep = 0.1

# individuals
ni_sust = 50  # number of agents with sustainable behaviour 1
ni_nonsust = 50 # number of agents with unsustainable behaviour 0
nindividuals = ni_sust + ni_nonsust

# cells:
cell_stock=1
cell_capacity=1
cell_growth_rate=1
nc = nindividuals  # number of cells

#groups:
ng_total = 10 # number of total groups
ng_sust = 5 # number of sustainable groups
ng_nonsust = ng_total - ng_sust
group_meeting_interval = 1

#networks
acquaintance_network_type = "Erdos-Renyi"
group_membership_network_type = "Erdos-Renyi"
p = 0.5  # link density for random networks



#---write into dic---
configuration = {
    "seed": seed,
    "timeinterval": timeinterval,
    "timestep" : timestep,
    "ni_sust" : ni_sust,
    "ni_nonsust" : ni_nonsust,
    "nindividuals" : nindividuals,
    "cell_stock": cell_stock,
    "cell_capacity": cell_capacity,
    "cell_growth_rate": cell_growth_rate,
    "nc" : nc,
    "ng_total" : ng_total,
    "ng_sust" : ng_sust,
    "ng_nonsust" : ng_nonsust,
    "group_meeting_interval" : group_meeting_interval,
    "acquaintance_network_type" : acquaintance_network_type,
    "group_membership_network_type" : group_membership_network_type,
    "p" : p
}

#---save json file---
f = open("configuration", "w+")
json.dump(configuration, f, indent=4)
