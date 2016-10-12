# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of subclass Equal_Distributor.
"""

#
#  Imports
#

from abstract_group import Group

#
#  Define class MacroAgents
#


class Equal_Distributor(Group):
    """
    Encapsulates states and dynamics of subclass Equal_Distributors.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 group_identifier,
                 territories,
                 member,
                 group_stock,
                 group_harvest,
                 group_strategy):
        """
        Initializes an instance of an 'Equal_Distributor'. Inherits
        group_identifier, territories and member from class 'Group'.
        Generates group_stock, group_harvest, group_strategy.
        """
        super(Equal_Distributor, self).__init__(group_identifier, 
                                                territories,
                                                member
                                                )
        self.group_stock = None
        self.group_harvest = None 
        self.group_strategy = None 

    def __str__(self)
        """
        Returns a string representation of the object of class
        'Equal_Distributor'.
        """
        return (super(Equal_Distributor, self).__str__() +
                ('group_stock % s, \
                 group_harvest % s, \
                 group_strategy % s'
                 ) % (
                 self.group_stock,
                 self.group_harvest,
                 self.group_strategy
                 )
                )

    def set_group_stock(self, group_stock):
        """
        A function to set the total stock of a group.
        """
        self.group_stock = group_stock

    def set_group_harvest(self, group_harvest):
        """
        A function to set the total harvest of a group.
        """
        self.group_harvest = group_harvest

    def set_group_strategy(self, group_strategy):
        """
        A function to set the group's strategy.
        """
        self.group_strategy = group_strategy

    #
    #  Definitions of further methods
    #

    

    def calculate_deathrate():
        """
        Method to calculate the deathrate in dependence of the harvest
        """

    def calculate_birthrate():
        """
        Method to calculate the birthrate in dependece of the harvest
        """
