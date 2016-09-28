# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of social macro agents.
"""

#
#  Imports
#

#
#  Define class MacroAgents
#


class Groups(object):
    """
    Encapsulates states and dynamics of social macro agents.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 group_identifier,
                 territories,
                 member):
        """
        Initialize an instance of MacroAgents.
        """

        self.group_identifier = group_identifier
        self.territories = None
        self.member = None

    def __str__(self):
        """
        Return a string representation of the object of class individual
        """
        return ('Group with identifier % s, \
                territories % s, \
                member % s'
                ) % (
                self.group_identifier,
                self.territories,
                self.member)

    def set_territories(self, territories):
        """
        a function to set the territories of a group, territories is a list
        of cell_identifiers
        """
        self.territories = territories

    def set_member(self, member):
        """
        A function that generates a List with all members and the
        following information: individual_identifier
        """
        self.member = member

    #
    #  Definitions of further methods
    #

    def get_population(self, member):
        """
        Method to get the amount of individuals in the society. Necessary to
        calculate the total harvest.
        """
        return len(self.member)
