# This is a first test model to set initial conditions

#
# Imports
#

import numpy as np
from cells import abstract_cells
from groups import abstract_groups
from individuals import abstract_individuals

#
# Model execution
#


def Build_World(N_i,
                N_g,
                N_c
                ):
    """
    Build a world with N_c cells, N_g groups and N_i individuals
    """

    List_c = [
        abstract_cells.Cells(i, None) for i in range(N_c)]

    List_i = [
        abstract_individuals.Individuals(i, None, None) for i in range(N_i)]

    List_g = [
        abstract_groups.Groups(i, None, None) for i in range(N_g)]

    # Groups distributed to cells randomly
    for i in range(0, N_g):
        if N_g > N_c:
            print 'More groups than cells'
            break
        else:
            x = np.zeros(shape=(N_c, 1))
            x[i, 0] = i
            List_g[i].set_territories(x)

    # Match individuals and Groups
    big_list = np.zeros(shape=(N_i,3))
    for i in range(N_i):
        # Chose one group at random
        p1 = np.random.randint(0, N_g)
        # Check out how many territories this group owns
        a = np.where(List_g[p1].territories != 0)[0])
        b = len(a)
        # Chose on territory at random
        p2 = np.random.randint(0, b)
        c = a[0][p2]
        # Assigne individual to group
        List_i[i].set_group_identifier(p1)
        # Assigne cell to individual
        List_i[i].set_cell_identifier(c)
        # Writing into biglist
        big_list[i,0] = i
        big_list[i,1] = p1
        big_list[i,2] = c

    #
    # Create the Memberlist for each group, containing individual idents and
    # their cell identifier
    #
    # Aim of the following for-loop is to creat a memberlist that contains
    # the members of each group. For this we re looking at the above
    # defined big_list that contains all necessary information.
    # WE STILL NEED TO THINK THROUGH THAT PART
    #

    for i in range(N_g):
        memberlist = np.zeros(shape=(N_i, 2))
        for j in range(N_i):
            if big_list[j,1] == i:
               memberlist[j, 0] = big_list[j, 0]
               memberlist[j, 1] = big_list[j, 2]
        List_g[i].set_member(memberlist)



    print 'this is cell 1 ? ', List_c[1]
    print 'this is individual 0?', List_i[0]
    print 'this is group 2', List_g[2]
Build_World(5, 3, 5)
    

