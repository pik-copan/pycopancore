import random as rd

import numpy as np
from numba import njit


@njit
def _set_numba_seed(seed):
    """helper function"""
    rd.seed(seed)
    np.random.seed(seed)


def set_seed(seed):
    """Set a global seed to be used for the python random package and
    the numpy.random package, in both normal and numba-jitted functions
    """
    rd.seed(seed)
    np.random.seed(seed)
    _set_numba_seed(seed)
