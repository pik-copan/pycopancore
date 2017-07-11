"""Society entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
# from .... import master_data_model as D


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 municipality_like=False,
                 pareto_distribution_type=False,
                 **kwargs):
        """Initialize an instance of Society."""
        super().__init__(**kwargs)  # must be the first line

        self.municipality_like = municipality_like
        self.pareto_distribution_type = pareto_distribution_type

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def income_pdf(self):
        "Get probability density funtion of income and farm size."
        if self.pareto_distribution_type is False:
            # Use log-normal
            return
        if self.pareto_distribution_type is True:
            # Use pareto:
            return "not implemented yet"

    @property
    def pdf_mu(self):
        """Get mu of the log-normal distribution"""
        return

    @property
    def pdf_sigma(self):
        """Get the sigma of the log-normal distribution"""
        return

    @property
    def pdf_y_min(self):
        """get the y_min of the Pareo distribution"""
        return

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
