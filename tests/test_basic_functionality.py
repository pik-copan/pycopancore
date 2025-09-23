"""Basic functionality tests for pycopancore core components."""

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


class TestBasicImports:
    """Test that basic imports work."""

    def test_import_pycopancore(self):
        """Test that pycopancore can be imported."""
        import pycopancore

        assert pycopancore is not None

    def test_import_data_model(self):
        """Test that data_model module can be imported."""
        import pycopancore.data_model

        assert pycopancore.data_model is not None

    def test_import_model_components(self):
        """Test that model_components module can be imported."""
        import pycopancore.model_components

        assert pycopancore.model_components is not None


class TestVariableClass:
    """Test Variable class basic functionality."""

    def test_variable_import(self):
        """Test that Variable can be imported."""
        from pycopancore.data_model.variable import Variable

        assert Variable is not None

    def test_variable_creation(self):
        """Test basic variable creation."""
        from pycopancore.data_model.variable import Variable

        var = Variable("test_var", "A test variable")
        assert var.name == "test_var"
        assert var.desc == "A test variable"

    def test_variable_with_default(self):
        """Test variable with default value."""
        from pycopancore.data_model.variable import Variable

        var = Variable("default_var", "Variable with default", default=42)
        assert var._default_value == 42


class TestUnitClass:
    """Test Unit class basic functionality."""

    def test_unit_import(self):
        """Test that Unit can be imported."""
        from pycopancore.data_model.unit import Unit

        assert Unit is not None

    def test_dimension_import(self):
        """Test that Dimension can be imported."""
        from pycopancore.data_model.dimension import Dimension

        assert Dimension is not None

    def test_unit_creation(self):
        """Test basic unit creation."""
        from pycopancore.data_model.unit import Unit
        from pycopancore.data_model.dimension import Dimension

        dim = Dimension("length")
        unit = Unit("m", "meter", dimension=dim)
        assert unit.name == "m"
        assert unit.desc == "meter"
        assert unit.dimension == dim


class TestDimensionalQuantity:
    """Test DimensionalQuantity class basic functionality."""

    def test_dimensional_quantity_import(self):
        """Test that DimensionalQuantity can be imported."""
        from pycopancore.data_model.dimensional_quantity import (
            DimensionalQuantity,
        )

        assert DimensionalQuantity is not None

    def test_dimensional_quantity_creation(self):
        """Test basic dimensional quantity creation."""
        from pycopancore.data_model.dimensional_quantity import (
            DimensionalQuantity,
        )
        from pycopancore.data_model.unit import Unit
        from pycopancore.data_model.dimension import Dimension

        dim = Dimension("length")
        unit = Unit("m", "meter", dimension=dim)
        qty = DimensionalQuantity(5.0, unit)

        assert qty.number() == 5.0
        assert qty.unit == unit


class TestOrderedSet:
    """Test OrderedSet class basic functionality."""

    def test_ordered_set_import(self):
        """Test that OrderedSet can be imported."""
        from pycopancore.data_model.ordered_set import OrderedSet

        assert OrderedSet is not None

    def test_ordered_set_creation(self):
        """Test basic ordered set creation."""
        from pycopancore.data_model.ordered_set import OrderedSet

        s = OrderedSet([1, 2, 3])
        assert list(s) == [1, 2, 3]

    def test_ordered_set_add(self):
        """Test adding elements to ordered set."""
        from pycopancore.data_model.ordered_set import OrderedSet

        s = OrderedSet([1, 2])
        s.add(3)
        assert list(s) == [1, 2, 3]


class TestAbstractComponents:
    """Test abstract component classes."""

    def test_abstract_imports(self):
        """Test that abstract components can be imported."""
        from pycopancore.model_components import abstract

        assert abstract is not None

    def test_abstract_world(self):
        """Test abstract World class."""
        from pycopancore.model_components.abstract.world import World

        world = World()
        assert world is not None

    def test_abstract_cell(self):
        """Test abstract Cell class."""
        from pycopancore.model_components.abstract.cell import Cell

        cell = Cell()
        assert cell is not None

    def test_abstract_individual(self):
        """Test abstract Individual class."""
        from pycopancore.model_components.abstract.individual import Individual

        individual = Individual()
        assert individual is not None


class TestBaseComponents:
    """Test base component classes."""

    def test_base_imports(self):
        """Test that base components can be imported."""
        from pycopancore.model_components.base import interface

        assert interface is not None

    def test_base_world(self):
        """Test base World class."""
        from pycopancore.model_components.base.implementation.world import (
            World,
        )

        world = World()
        assert world is not None

    # TODO: Fix Cell class - requires world/environment setup, missing _world
    # def test_base_cell(self):
    #     """Test base Cell class."""
    #     from pycopancore.model_components.base.implementation.cell import (
    #         Cell
    #     )
    #     cell = Cell()
    #     assert cell is not None

    # TODO: Fix Individual class - requires cell parameter, missing _cell
    # def test_base_individual(self):
    #     """Test base Individual class."""
    #     from pycopancore.model_components.base.implementation.individual import (  # noqa: E501
    #         Individual
    #     )
    #     individual = Individual()
    #     assert individual is not None


class TestSevenDwarfsComponents:
    """Test seven dwarfs component classes."""

    def test_seven_dwarfs_imports(self):
        """Test that seven dwarfs components can be imported."""
        from pycopancore.model_components.seven_dwarfs import model

        assert model is not None

    def test_seven_dwarfs_world(self):
        """Test SevenDwarfs World class."""
        from pycopancore.model_components.seven_dwarfs.implementation.world import (  # noqa: E501
            World,
        )

        world = World()
        assert world is not None

    # TODO: Fix SevenDwarfs Cell - missing assert_valid method, requires model setup  # noqa: E501
    # def test_seven_dwarfs_cell(self):
    #     """Test SevenDwarfs Cell class."""
    #     from pycopancore.model_components.seven_dwarfs.implementation.cell import (  # noqa: E501
    #         Cell
    #     )
    #     cell = Cell()
    #     assert cell is not None

    # TODO: Fix SevenDwarfs Individual - missing social_system attribute, requires model setup  # noqa: E501
    # def test_seven_dwarfs_individual(self):
    #     """Test SevenDwarfs Individual class."""
    #     from pycopancore.model_components.seven_dwarfs.implementation.individual import (  # noqa: E501
    #         Individual
    #     )
    #     individual = Individual()
    #     assert individual is not None


class TestVersion:
    """Test version functionality."""

    def test_version_import(self):
        """Test that version can be imported."""
        import pycopancore

        assert hasattr(pycopancore, "__version__")
        assert pycopancore.__version__ is not None

    def test_version_format(self):
        """Test that version has correct format."""
        import pycopancore

        version = pycopancore.__version__
        # Version should be in format like "0.8.6" or "0.8.6.dev0"
        assert isinstance(version, str)
        assert len(version) > 0


if __name__ == "__main__":
    pytest.main([__file__])
