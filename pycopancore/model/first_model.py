# This is a first test model to set initial conditions

#
# Imports
#

import numpy as np
from pycopancore.cell.local_renewable_resource import RenewableResource as rr
from pycopancore.cell.donut_world import DonutWorld as dw
from pycopancore.group.equal_distributor import EqualDistributor as ed
# from .group import Subclass of Metabolism?
from pycopancore.individual.binary_social_learner import BinarySocialLearner\
     as bsl
from pycopancore.individual.exploit_like import ExploitLike as el
from pycopancore.model.abstract_model import Model

#
# Model execution/Define class FirstModel
#


class FirstModel(Model):
    """
    This will be a simple model to test if all classes work together properly
    """

    def __init__(self,
                 number_individuals,
                 number_groups,
                 number_cells,
                 width_grid,
                 height_grid
                 ):
        """
        Build a world 

        Parameters
        ----------
        number_individuals : integer
            The desired number of individuals
        number_groups : integer
            The number of groups, should be smaller or equal to the number of
            cells
        number_cells: integer
            The number of cells, should be larger or equal to the number of
            groups
        width_grid: integer
            The width of the grid of cells. Width*eight must be equal to
            number_cells
        heigth_grid: integer
            The height of the grid of cells. Width*eight must be equal to
            number_cell
        """

        self.number_individuals = number_individuals
        self.number_groups = number_groups
        self.number_cells = number_cells
        self.width_grid = width_grid
        self.height_grid = height_grid

        assert (width_grid*height_grid) == number_cells

        # Create Grid of Cells of Subclass RenewableResource
        DW = dw()
        List_c = DW.create_grid(width_grid, height_grid)

        # Create Individuals of Subclass BinarySocialLearner
        EL = el()
        List_i = EL.create_individuals(number_individuals)


        # Create Groups of Subclass EqualDistributor
        List_g = [
            ed(i) for i in range(number_groups)]
    
        # Groups distributed to cells
        for i in range(0, number_groups):
            if number_groups > number_cells:
                print ('More groups than cells')
                break
            else:
                x = np.full((number_cells, 1), np.nan)
                x[i, 0] = i
                List_g[i].set_territories(x)

        # Match Individuals and Groups
        all_individuals_ident = []
        all_individuals_cell = []
        all_individuals_group = []
        for i in range(number_individuals):
            # Chose one group at random
            p1 = np.random.randint(0, number_groups)
            # Check out how many territories this group owns
            a = np.where(np.isnan(List_g[p1].territories) == False)[0]
            b = len(a)
            # Chose on territory at random
            p2 = np.random.random_integers(0, b-1)
            c = a[p2]
            # Assigne individual to group
            List_i[i].set_group_affiliation(p1)
            # Assigne cell to individual
            List_i[i].set_cell_affiliation(c)
            # Writing into lists
            all_individuals_ident.append(i)
            all_individuals_group.append(p1)
            all_individuals_cell.append(c)

        #
        # Create the Memberlist for each group, containing individual idents
        # and their cell identifier
        #

        for i in range(0, number_groups):
            memberlist = []
            if all_individuals_group.count(i) == 0:
                # assure group has a member to evade error in .index-func
                continue
            else:
                # get indices of all individuals in the i'th group
                a = [y for y, val in enumerate(all_individuals_group) \
                     if val == i]
                for j in a:
                    memberlist.append((all_individuals_ident[j],
                                    all_individuals_cell[j]))
            List_g[i].set_member(memberlist)

        #
        # Create connections between Individuals
        #

        EL.create_network(List_i, 1, 0.5)

        #
        # Make Metabolism
        #



        print ('this is cell 1:', List_c[1])
        print ('this is individual 9:', List_i[9])
        print ('this is group 2:', List_g[2])
