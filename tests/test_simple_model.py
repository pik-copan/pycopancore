#
# This is the unittest of the first_model file, and, since this is a model,
# of the whole structure
#

from pycopancore import FirstModel as fm


def test_setup():
    fm(50, 6, 6, 3, 2)
