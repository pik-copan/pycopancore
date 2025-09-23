"""
==========
Data model
==========

**************************
Variable naming convention
**************************

We suggest to use rather descriptive variable names that make the relevant
dimension clear in the following fashion:

* Variables that represent integer cardinalities should be called
  **numbers** (possibly abbreviated as `n`, `no`, or `num`) or **counts**.

* Extensive variables of simple physical dimension should be called **stocks**,
  e.g. `atmospheric_carbon_stock` of dimension `carbon` and default unit
  `GtC`, or `physical_capital_stock` of dimension `monetary_value` and
  default unit `dollars`.

* Intensive variables of simple physical dimension should *not* be called
  'stocks' to distinguish them from extensive variables. E.g.
  `surface_air_temperature` of dimension `temperature` and default unit
  `kelvins`.

* Variables that represent a stock per surface area, volume, or mass should
  be called **densities**, e.g., `vegetation_carbon_density` in `GtC/m2` or
  `energy_density_of_wood` in `MJ/kg`.

* Variables that represent (changes of) stocks per time or time derivatives
  of stocks should be called **flows**, e.g. `photosynthesis_carbon_flow` of
  dimension `carbon/time` and default unit `GtC/yr`, or `income_flow` of
  dimension `money/time` and default unit `dollars/yr`.

* Variables that represent flows per surface area should be called **fluxes**,
  e.g. `sensible_heat_flux` of dimension `energy/time/area` and default unit
  `W/m^2`.

* Variables of dimension `time` that represent specific unique time points
  should be called **time_points** or **dates**, e.g., `net_zero_date`.

* Variables of dimension `time` that represent amounts of time *between*
  time points should be called **delays**, **intervals**, **durations**,
  **periods**, **ages**, etc., or sometimes just **times**.
  e.g. `business_cycle_period` or `Individual.age`.

* Variables of dimension `1/time` referring to periodic occurrences should be
  called **frequencies**, i.e., `voting_frequency`.

* Other variables of dimension `1/time` should be called **rates**, e.g.
  `equilibration_rate`, `discount_rate`, `depreciation_rate`,
  `diffusion_rate`. Variables of other dimension than `1/time`, in particular
  fractions or ratios, should *not* be called 'rates'.

* Dimensionless variables between 0 and 1 that represent parts of a whole
  should be called **fractions** or **shares**, e.g. `dirty_fraction` or
  `fossil_energy_share`.

* Dimensionless variables that represent the relative size of one quantity
  as compared to another quantity of the same dimension should be called
  **ratios**, e.g., `cost_benefit_ratio`.

* Variables representing the derivative of one quantity w.r.t. another
  quantity (other than time) should be called **sensitivities**, e.g.
  `temperature_sensitivity_of_photosynthesis`.

* Variables representing the derivative of the *logarithm* of one quantity
  w.r.t. the logarithm of another quantity should be called **elasticities**,
  e.g. `labor_elasticity_of_fossil_energy_production`.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# Core data model components
from .variable import Variable
from .unit import Unit
from .dimension import Dimension
from .dimensional_quantity import DimensionalQuantity
from .ordered_set import OrderedSet
from .reference_variable import ReferenceVariable
from .set_variable import SetVariable

# Note: master_data_model is imported by other modules as needed
