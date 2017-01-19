from pycopancore.model_components.base import Cell

a = Cell()


def test_location():
    """
    Test if the instance of Cell has a location
    :return:
    """
    assert a.location == (0, 0), "Location is not (0,0)"
