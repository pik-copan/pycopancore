import numpy as np


__author__ = 'marie'


def lower_triangular(a):
    """
    check if array is lower triangular matrix
    :param a: arbitrary matrix
    :return: True, if it is lower triangular; False, otherwise
    """
    [_, n] = np.shape(a)

    for i in range(n):
        for j in range(i+1, n):
            if a[i, j] != 0:
                return False

    return True


def strict_lower_triangular(a):
    """
    check if array is strict lower triangular matrix
    :param a: arbitrary matrix
    :return: True, if it is a strictly lower triangular matrix; False, otherwise
    """
    [_, n] = np.shape(a)

    for i in range(n):
        for j in range(i, n):
            if a[i, j] != 0:
                return False

    return True


def upper_triangular(a):
    """
    check if array is upper triangular matrix
    :param a: arbitrary matrix
    :return: True, if it is upper triangular; False, otherwise
    """
    [m, n] = np.shape(a)

    for i in range(n):
        for j in range(i+1, m):
            if a[j, i] != 0:
                return False

    return True


def strict_upper_triangular(a):
    """
    check if array is strict upper triangular matrix
    :param a: arbitrary matrix
    :return: True, if it is strictly upper triangular; False, otherwise
    """
    [m, n] = np.shape(a)

    for i in range(n):
        for j in range(i, m):
            if a[j, i] != 0:
                return False

    return True


def diagonal(a):
    """
    check if array is diagonal matrix (Note: a zero-matrix is diagonal too!)
    :param a: arbitrary matrix
    :return: True, if it is diagonal; False, otherwise
    """
    return lower_triangular(a) & upper_triangular(a)


def diagonal_and_nonzero(a):
    """
    check if array is diagonal matrix and non-zero
    :param a: arbitrary matrix
    :return: True, if it is diagonal with non-zero entries; False, otherwise
    """

    assert diagonal(a)

    return non_zero_diagonal(a)


def non_zero_diagonal(a):
    """
    check if diagonal entries are non-zero
    :param a: arbitrary matrix
    :return: True, if diagonal entries are non-zero; False, otherwise
    """

    [m, n] = np.shape(a)

    for i in range(np.min([m, n])):
        if a[i, i] == 0:
            return False

    return True
