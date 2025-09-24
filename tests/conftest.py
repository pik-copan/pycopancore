"""Pytest configuration for pycopancore tests."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import pytest
import numpy as np


@pytest.fixture
def sample_world():
    """Create a sample World instance for testing."""
    from pycopancore.model_components.base import World

    return World()


@pytest.fixture
def sample_cell():
    """Create a sample Cell instance for testing."""
    from pycopancore.model_components.base import Cell

    return Cell()


@pytest.fixture
def sample_individual():
    """Create a sample Individual instance for testing."""
    from pycopancore.model_components.base import Individual, Cell

    cell = Cell()
    return Individual(cell=cell)


@pytest.fixture
def sample_social_system():
    """Create a sample SocialSystem instance for testing."""
    from pycopancore.model_components.base import SocialSystem

    return SocialSystem()


@pytest.fixture
def sample_variable():
    """Create a sample Variable instance for testing."""
    from pycopancore.data_model import Variable

    return Variable("test_var", "A test variable")


@pytest.fixture
def sample_unit():
    """Create a sample Unit instance for testing."""
    from pycopancore.data_model import Unit, Dimension

    dim = Dimension("length")
    return Unit("m", "meter", dim)


@pytest.fixture
def sample_dimensional_quantity():
    """Create a sample DimensionalQuantity instance for testing."""
    from pycopancore.data_model import DimensionalQuantity, Unit, Dimension

    dim = Dimension("length")
    unit = Unit("m", "meter", dim)
    return DimensionalQuantity(5.0, unit)
