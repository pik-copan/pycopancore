# This is a first test model to set initial conditions

#
# Imports
#

import numpy as np

from .. import Cell
from .. import Group
from .. import Individual

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
        abstract_cell.Cell(i, None) for i in range(N_c)]

    List_i = [
        abstract_individual.Individual(i, None, None) for i in range(N_i)]

    List_g = [
        abstract_group.Group(i, None, None) for i in range(N_g)]

    # Groups distributed to cells randomly
    for i in range(0, N_g):
        if N_g > N_c:
            print ('More groups than cells')
            break
        else:
            x = np.full((N_c, 1), np.nan)
            x[i, 0] = i
            List_g[i].set_territories(x)

    # Match individuals and Groups
    big_list = np.full((N_i, 3), np.nan)
    for i in range(N_i):
        # Chose one group at random
        p1 = np.random.randint(0, N_g)
        # Check out how many territories this group owns
        a = np.where(List_g[p1].territories != np.nan)[0]
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
        big_list[i, 0] = i
        big_list[i, 1] = p1
        big_list[i, 2] = c

    #
    # Create the Memberlist for each group, containing individual idents and
    # their cell identifier
    #

    for i in range(N_g):
        memberlist = np.full((N_i, 2), np.nan)
        for j in range(N_i):
            if big_list[j, 1] == i:
                memberlist[j, 0] = big_list[j, 0]
                memberlist[j, 1] = big_list[j, 2]
        List_g[i].set_member(memberlist)

    print ('this is cell 1 ? ', List_c[1])
    print ('this is individual 0?', List_i[0])
    print ('this is group 2', List_g[2])
Build_World(5, 3, 5)
