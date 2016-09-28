# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Takes the different classes and generates a model
"""

#
# Imports
#

# from .abstract_groups import Groups
# from .abstract_individuals import Individuals
from .abstract_cells import Cells

#
# Define the models properties
#

# Start by generating cells


def generate_cells(N):
    """
    Generate N cells of a class
    """
    list_cells = [Cells(i) for i in range(N)]
<<<<<<< HEAD:pycopancore/models/simple_model.py
    print list_cells[1].cell_identifier
    return list_cell
=======
    print (list_cells[1].cell_identifier)
    return list_cells
>>>>>>> till:models/simple_model.py
