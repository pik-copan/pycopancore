# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license
# das habe ich veraendert


"""
Encapsulates states and dynamics of social micro agents.
"""

#
#  Imports
#


#
#  Define class Individual
#

class Individual(object):
    """
    Encapsulates states and dynamics of social micro agents.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 individual_identifier,
                 group_affiliation,
                 cell_affiliation
                 ):
        """
        Initialize an instance of MicroAgents.
        The object_identifier variables are numbers to identify each object.
        The behavour_dict includes information about behaviour
        The connection_dict includes the identifers of connected individuals

        Parameters
        ----------
        individual_identifier : integer
            this is a number which identifies each individual
        group_affiliation : integer
            this is a number which indicates to which group the individual
            is affiliated
        cell_affiliation : integer
            this is a number which indicates to which cell the individual
            is affiliated
        """

        self.individual_identifier = individual_identifier
        self.group_affiliation = None
        self.cell_affiliation = None

    def __str__(self):
        """
        Return a string representation of the object of class individual
        """
        return ('Individual with identifier % s, \
                group % s, \
                cell % s '
                ) % (
                self.individual_identifier,
                self.group_affiliation,
                self.cell_affiliation)

    def set_cell_affiliation(self, cell_affiliation):
        """
        A function to set the location or cell of an individual
        """
        self.cell_affiliation = cell_affiliation

    def set_group_affiliation(self, group_affiliation):
        """
        A function to set the group membership of an individual
        """
        self.group_affiliation = group_affiliation

    #
    #  Definitions of further methods
    #
