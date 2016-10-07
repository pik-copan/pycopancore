# This is a first test model to set initial conditions

#
# Imports
#

import numpy as np
from cell import abstract_cell
from group import abstract_group
from individual import abstract_individual

#
# Model execution
#


def Build_World(N_i,
                N_g,
                N_c,
                k
                ):
    """
    Build a world with N_c cells, N_g groups and N_i individuals. The average 
    degree of the individuals in the network is k.
    """

    List_c = [
        abstract_cell.Cell(i, None, None) for i in range(N_c)]

    List_i = [
        abstract_individual.Individual(i,
                                       None,
                                       None,
                                       None) for i in range(N_i)]

    List_g = [
        abstract_group.Group(i, None, None) for i in range(N_g)]

    # Groups distributed to cells
    for i in range(0, N_g):
        if N_g > N_c:
            print ('More groups than cells')
            break
        else:
            x = np.full((N_c, 1), np.nan)
            x[i, 0] = i
            List_g[i].set_territories(x)

    # Match individuals and Groups
    all_individuals_ident = []
    all_individuals_cell = []
    all_individuals_group = []
    for i in range(N_i):
        # Chose one group at random
        p1 = np.random.randint(0, N_g)
        # Check out how many territories this group owns
        a = np.where(np.isnan(List_g[p1].territories) == False)[0]
        b = len(a)
        # Chose on territory at random
        if b == 0:  # Accounts for random number generator intervall
            p2 = 0
        else:
            p2 = np.random.randint(0, b)
        c = a[p2]
        # Assigne individual to group
        List_i[i].set_group_identifier(p1)
        # Assigne cell to individual
        List_i[i].set_cell_identifier(c)
        # Writing into biglist
        all_individuals_ident.append(i)
        all_individuals_group.append(p1)
        all_individuals_cell.append(c)

    #
    # Create the Memberlist for each group, containing individual idents and
    # their cell identifier
    #

    for i in range(0, N_g + 1):  # Account for closed interval
        memberlist = []
        if all_individuals_group.count(i) == 0:
            # assure group has a member to evade error in .index-func
            continue
        else:
            # get indices of all individuals in the i'th group
            a = [y for y, val in enumerate(all_individuals_group) if val == i]
            for j in a:
                memberlist.append((all_individuals_ident[j],
                                  all_individuals_cell[j]))
        List_g[i].set_member(memberlist)

    #
    # Create connections between Individuals
    #

    N_c = (k * N_i)/2
    N_co = 0
    while N_co <= N_c:
        # Chose individual by random
        i_1 = np.random.randint(0, N_i)
        i_2 = np.random.randint(0, N_i)
        if i_1 == i_2:
            # Check for self-connection
            continue
        if  i_2 in List_i[i_1].connections:
            # Check for double-connection
            continue
        List_i[i_1].add_connection(i_2)
        List_i[i_2].add_connection(i_1)
        N_co += 1





    print ('this is cell 1:', List_c[1])
    print ('this is individual 9:', List_i[9])
    print ('this is group 2:', List_g[2])

Build_World(10, 5, 5, 3)
