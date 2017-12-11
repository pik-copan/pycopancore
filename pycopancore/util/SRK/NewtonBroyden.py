import numpy as np
from numba import jit
import scipy.optimize as sc


__author__ = 'marie'


# extracted from Frank's solver TODO: check


def newton_broyden(fun, x_0, jac_inv=None, reltol=1e-6, abstol=1e-8, max_newton=10, force_full_compile=False):
    """
    Implementing Newton-Broyden Method
    :param fun: function handle for which roots need to be found
    :param x_0: first guess for root; value to find close by root
    :param reltol: relative tolerance
    :param abstol: absolute tolerance
    :param max_newton: maximum number of newton iterations
    :param force_full_compile: force full compilation via numba.jit if True; default: False
    """

    # set before some information
    system_dimension = np.size(x_0)
    identity = np.eye(system_dimension)

    # define functions for pre-compilation

    # guess Jacobi via Difference-Quotient
    @jit(nopython=force_full_compile)
    def guess_jac(f, x_0):
        """
        Computes a first initial guess Jacobi-Inverse of function f at point x_0
        :param f: function handle whose Jacobi-Inverse shall be approximated
        :param x_0: point at which the Jacobi shall be approximated
        :return: initial guess of Jacobi-Inverse
        """
        x_0 = np.array(x_0)
        n = np.size(x_0)
        jac = np.empty((n, n), dtype=np.float64)

        for i in range(n):

            if not x_0[i] == 0.:
                d = 2 ** (-11) * x_0[i]
            else:
                d = 2 ** (-11)

            jac[:, i] = (f(x_0 + d*identity[i]) - f(x_0)) / d

        return jac

    # do one newton step (x-J_inv*f)
    @jit(nopython=force_full_compile)
    def newton_step(x, f, jac_inv):
        """
        Do a Newton-step
        :param x:
        :param f:
        :param jac_inv:
        :return:
        """
        return x - np.dot(jac_inv, f)

    # broyden update of J_inv, not using matrix multiplication because of stupid python
    # Grewank-Andreas-Broyden.pdf Formula (6)
    @jit(nopython=force_full_compile)
    def broyden_update(jac_inv, minus_delta_x, delta_fun):

        norm_inv = np.dot(delta_fun, delta_fun)
        if norm_inv < 1e-9:
            return jac_inv

        norm = 1. / norm_inv
        minus_update = norm * (minus_delta_x + np.dot(jac_inv, delta_fun))
        for i in range(system_dimension):
            for j in range(system_dimension):
                jac_inv[i, j] -= minus_update[i] * delta_fun[j]

        return jac_inv

    # check whether the residual is small enough
    @jit(nopython=force_full_compile)
    def residue_is_small(f, x):
        # print np.abs(np.max(f))
        for i in range(system_dimension):
            if np.abs(f[i]) > reltol * np.abs(x[i]) + abstol:
                return False

        return True

    # start algorithm

    # compute inverse of Jacobian
    if jac_inv is None:
        # print("Guessing Jac")
        jac = guess_jac(fun, x_0)
        # print("I'm only here for a breakpoint")
        jac_inv = np.linalg.inv(jac)

    # reserve temporary variables for computation
    x = np.empty((2, system_dimension), dtype=np.float64)
    r = np.empty((2, system_dimension), dtype=np.float64)

    # Take an explicit newton step to get started:
    x[1] = x_0
    r[1] = fun(x_0)
    # Newton step:
    n = np.dot(jac_inv, r[1])
    x[0] = x[1] - n
    r[0] = fun(x[0])
    j = 0
    success = False

    # Iterate Newton-Broyden if needed:

    while j < max_newton and not success:
        jac_inv = broyden_update(jac_inv, n, r[j % 2] - r[(j + 1) % 2])
        # Newton step:
        n = np.dot(jac_inv, r[j % 2])
        x[(j + 1) % 2] = x[j % 2] - n
        r[(j + 1) % 2] = fun(x[(j + 1) % 2])
        if residue_is_small(r[(j + 1) % 2], x[(j + 1) % 2]):
            success = True
        j += 1

    # If the first iteration does not succeed, update the inverse Jacobian explicitly and take a step:
    if not success:
        jac_inv = np.linalg.inv(guess_jac(fun, x[j % 2]))
        # Newton step:
        n = np.dot(jac_inv, r[j % 2])
        x[(j + 1) % 2] = x[j % 2] - n
        r[(j + 1) % 2] = fun(x[(j + 1) % 2])
        if residue_is_small(r[(j + 1) % 2], x[(j + 1) % 2]):
            success = True
        j += 1

    # If this was not sufficient, start iterating one more time starting from the updated Jacobian.
    while j < 2 * max_newton and not success:
        jac_inv = broyden_update(jac_inv, n, r[j % 2] - r[(j + 1) % 2])
        # Newton step:
        n = np.dot(jac_inv, r[j % 2])
        x[(j + 1) % 2] = x[j % 2] - n
        r[(j + 1) % 2] = fun(x[(j + 1) % 2])
        if residue_is_small(r[(j + 1) % 2], x[(j + 1) % 2]):
            success = True
        j += 1

    # If the second iteration does not succeed, update the inverse Jacobian explicitly and take a step:
    if not success:
        jac_inv = np.linalg.inv(guess_jac(fun, x[j % 2]))
        # Newton step:
        n = np.dot(jac_inv, r[j % 2])
        x[(j + 1) % 2] = x[j % 2] - n
        r[(j + 1) % 2] = fun(x[(j + 1) % 2])
        if residue_is_small(r[(j + 1) % 2], x[(j + 1) % 2]):
            success = True
        j += 1

    # If this was not sufficient, start iterating one more time starting from the updated Jacobian.
    while j < 100 and not success:
        jac_inv = broyden_update(jac_inv, n, r[j % 2] - r[(j + 1) % 2])
        # Newton step:
        n = np.dot(jac_inv, r[j % 2])
        x[(j + 1) % 2] = x[j % 2] - n
        r[(j + 1) % 2] = fun(x[(j + 1) % 2])
        if residue_is_small(r[(j + 1) % 2], x[(j + 1) % 2]):
            success = True
        j += 1

    if success:
        return x[j % 2], jac_inv
    else:
        print("Convergence failure")
        return x[j % 2], jac_inv


def f(x):
    return np.sin(x)


#print('newton_krylov:', sc.newton_krylov(f, .5), 'newton_broyden:', newton_broyden(np.sin, np.array([2., .3, .2, .3])))
