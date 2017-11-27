"""model component Interface template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO: use variables from the master data model wherever possible:
from ... import master_data_model as D
from ...data_model.master_data_model import CUL, I, S
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "environmental awareness"
    """a unique name for the model component"""
    description = "Declining/growing terrestrial carbon increases likelihood" \
                    "of individuals becoming environmentally friendly/careless"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class SocialSystem (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    protected_terrestrial_carbon = S.protected_terrestrial_carbon
    protected_terrestrial_carbon_share = S.protected_terrestrial_carbon_share

    # exogenous variables / parameters:
    max_protected_terrestrial_carbon = \
        Variable("maximal protected stock of terrestrial carbon",
                 """what stock of the current terrestrial carbon would be treated
                 as protected if population is environmentally friendly""",
                 unit=D.gigatonnes_carbon, lower_bound=0,
                 default=0)


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    is_environmentally_friendly = I.is_environmentally_friendly

    # exogenous variables / parameters:


# process taxa:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:
    awareness_update_rate = \
        Variable("awareness update rate",
                 "rate at which a fraction of individuals update their " \
                 "awareness",
                 unit=D.years**-1, lower_bound=0, default=1)
    awareness_update_fraction = \
        Variable("awareness update fraction",
                 "fraction of individuals updating their awareness" \
                 "simultaneously",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=0.1)
    awareness_lower_carbon_density = \
        Variable("awareness lower carbon density",
                 "characteristic value of terrestrial carbon density below which " \
                 "individuals get more likely to become environmentally aware",
                 unit = D.gigatonnes_carbon / D.square_kilometers,
                 lower_bound=0, 
                 default=1e-5)  # ca. 2e-5 is the current global mean
    awareness_upper_carbon_density = \
        Variable("awareness upper carbon density",
                 "characteristic value of terrestrial carbon density above which " \
                 "individuals get more likely to become environmentally unaware",
                 unit = D.gigatonnes_carbon / D.square_kilometers,
                 lower_bound=0, 
                 default=2e-5)  # ca. 2e-5 is the current global mean
    max_protected_terrestrial_carbon_share = \
        Variable("maximal protected share of terrestrial carbon",
                 """what share of the current terrestrial carbon would be treated
                 as protected if population is environmentally friendly""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 default=0.5)  # TODO: a plausible value?
