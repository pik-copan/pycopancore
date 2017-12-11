from .Butcher import *
from numba import jit
import numpy as np
from .NewtonBroyden import newton_broyden as nb

import matplotlib.pyplot as plt


__author__ = 'marie'


# TODO: expand description !!!

# TODO: Speedy SRK, see Butcher below



# order 1.0 Butcher-Tableau
# butcher = Butcher(3)
#
# butcher.A = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# butcher.B1 = np.array([[0, 0, 0], [0.5, 0, 0], [0, 1, 0]])
# butcher.B2 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
# butcher.B3 = np.array([[0, 0, 0], [-1.5, 1, 0], [-1, 1, 0]])
# butcher.set_tableau()




'''
Solver for Stochastic(-Algebraic) Differential Equations using concept of Stochastic-Runge-Kutta (SRK) methods.

For simplicity the choice of Butcher-Tableau is restricted to diagonal implicit cases.
If no Butcher-Tableau is given, set a pre-defined order 0.5 SRK method.

The Butcher-Tableau for SRK methods is of the form

 c | A | B1 | B2 | B3
 --------------------
   | a | b1 | b2 | b3

the lower-case variables can be omitted by setting c = A e, where e = [1,...,1], and a = A_{s},
where A_{s} denotes the last row of A, same holds for B-matrices

If one want to use pre-defined Butcher-Tableau set butcher = 0.

For selecting needed type of SRK method add 'sde' or 'sdae'.

Note: for SDAE the sub-matrix A need to be invertible (or may have an explicit first stage with invertible sub-matrix);
      for SDE this conditions do not need to be met
'''

import numpy as np
from numba import jit
import scipy.optimize as sc


__author__ = 'marie'


# extracted from Frank's solver TODO: check


def newton_broyden(fun, x_0, reltol=1e-6, abstol=1e-8, max_newton=10, force_full_compile=False):
    """
    Implemeting Newton-Broyden Method
    :param fun: function handle for which roots need to be found
    :param x_0: first guess for root; value to find close by root
    :param reltol: relative tolerance
    :param abstol: absolute tolerance
    :param max_newton: maximum number of newton iterations
    :param force_full_compile: force full compilation via numba.jit if True; default: False
    """

    # set before some information

    # start algorithm

    # compute inverse of Jacobian
    jac_inv = np.linalg.inv(guess_jac(fun, x_0))

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

    def newton_broyden(x, r, jac_inv):

        x[1] = x_0
        r[1] = fun(x_0)
        # Newton step:
        n = np.dot(jac_inv, r[1])
        x[0] = x[1] - n
        r[0] = fun(x[0])
        j = 0
        success = False

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
            jac_inv = np.linalg.inv(guess_jac(x_0))
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

        if success:
            return x[j % 2]



def stochastic_runge_kutta_method(type, M, f, g, butcher, t, x_0):
    """
    Implements Stochastic Runge-Kutta method for a given or a fixed Butcher-Tableau.
    :param type: type of problem, 'sde' for SDE and 'sdae' for SDAE
    :param M: the singular matrix in front of SDAE-System, in case of SDE unused
    :param f: f(t,x) function handle for deterministic term
    :param g: g(t,x) function handle for stochastic term
    :param butcher: Butcher-tableau containing coefficients for solving method;
                    if want to use fixed Butcher-tableau give '0'
    :param t: time-series the method should find matching values for
    :param x_0: initial value

    :return: used time-series t and approximated solutions x
    """

    force_full_compile=False

    system_dimension = np.size(x_0)
    identity = np.eye(system_dimension)

    reltol = 1e-6
    abstol = 1e-8
    max_newton = 10

    # define functions for pre-compilation

    # guess Jacobi via Difference-Quotient
    @jit(nopython=force_full_compile)
    def guess_jac(fun, x_0):
        """
        Computes a first initial guess Jacobi-Inverse of function f at point x_0
        :param fun: function handle whose Jacobi-Inverse shall be approximated
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

            jac[:, i] = (fun(x_0 + d * identity[i]) - fun(x_0)) / d

        return jac

    # do one newton step (x-J_inv*f)
    @jit(nopython=force_full_compile)
    def newton_step(x, f_of_x, jac_inv):
        """
        Do a Newton-step
        :param x:
        :param f_of_x:
        :param jac_inv:
        :return:
        """
        return x - np.dot(jac_inv, f_of_x)

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
    def residue_is_small(f_of_x, x):

        for i in range(system_dimension):
            if np.abs(f_of_x[i]) > reltol * np.abs(x[i]) + abstol:
                return False

        return True

    def newton_broyden(fun, x_0, x, r, jac_inv):

        x[1] = x_0
        r[1] = fun(x_0)
        # Newton step:
        n = np.dot(jac_inv, r[1])
        x[0] = x[1] - n
        r[0] = fun(x[0])
        j = 0
        success = False

        while j < max_newton and not success:
            jac_inv = broyden_update(jac_inv, n, r[j % 2] - r[(j + 1) % 2])
            # Newton step:
            n = np.dot(jac_inv, r[j % 2])
            x[(j + 1) % 2] = x[j % 2] - n
            r[(j + 1) % 2] = fun(x[(j + 1) % 2])
            # r[(j + 1) % 2] = fun_ODE(X, x[i, :], t[i], H, dt, xi_n, j_s)
            if residue_is_small(r[(j + 1) % 2], x[(j + 1) % 2]):
                success = True
            j += 1

        # If the first iteration does not succeed, update the inverse Jacobian explicitly and take a step:
        if not success:
            jac_inv = np.linalg.inv(guess_jac(x_0))
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

        if success:
            return x[j % 2], jac_inv

    # reserve temporary variables for computation
    x_internal = np.empty((2, system_dimension), dtype=np.float64)
    r_internal = np.empty((2, system_dimension), dtype=np.float64)



    # assert right type of problem is inserted, else give hint
    assert type in ['sde', 'sdae'], "need to insert type of problem, 'sde' or 'sdae' "
    if type == 'sdae':
        if not len(x_0) == np.size(M, axis=1):
            raise TypeError('Matrix M need to fit size of initial value')

    # set a Butcher-Tableau, either insert and check given one or set fixed order 1.0 scheme
    # first, if no tableau is given
    if butcher == 0:

        butcher = Butcher(3)

        butcher.A = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        butcher.B1 = np.array([[0, 0, 0], [0.5, 0, 0], [0, 1, 0]])
        butcher.B2 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        butcher.B3 = np.array([[0, 0, 0], [-1.5, 1, 0], [-1, 1, 0]])
        butcher.set_tableau()

    # second, if tableau is given
    else:
        if type is 'sde':
            if not butcher.check_condition_sde():
                raise ValueError('The given SDE Butcher-Tableau is too complex!')
        elif type is 'sdae':
            if not butcher.check_condition_sdae():
                raise ValueError('The given SDAE Butcher-Tableau is too complex!')

        if not (butcher.check(0.5) | butcher.check(1.0)):
            raise ValueError('The given Butcher-Tableau is not valid.')

    # define needed variables

    # get number of steps
    N = len(t)

    # get needed information from Butcher-Tableau
    s = butcher.stages
    c = butcher.c
    A = butcher.A
    B1 = butcher.B1
    B2 = butcher.B2
    B3 = butcher.B3

    # set helpers and place-holder for solution
    n = np.size(x_0)
    H = np.zeros([s, n])
    x = np.zeros([N, n])
    x[0, :] = x_0

    # define pre-compiled function handles for later use
    @jit
    def fun_ODE(X, x, t, H, dt, xi_n, j):
        """
        define function handle to solve for case of SDE
        :param X: place-holder for unknown
        :param x: value of last step
        :param t: value of time-step before
        :param H: saves already known internal stages
        :param dt: current size of time-step
        :param xi_n: step-size of Wiener Process/ Brownian Motion
        :param j: current index of H_j to compute
        :return: function to solve
        """
        sqrt_dt = np.sqrt(dt)
        a = np.zeros(n)
        b = np.zeros(n)
        for k in range(j):
            a += A[j, k] * dt * f(t+c[j]*dt, H[k, :])
            b += (B1[j, k]*xi_n + B2[j, k]*0.5*(xi_n**2-sqrt_dt) + B3[j, k]*sqrt_dt)\
                * g(t+c[j]*dt, H[k, :])

        diag = A[j, j] * dt * f(t+c[j]*dt, X) + \
            (B1[j, j]*xi_n + B2[j, j]*0.5*(xi_n**2-sqrt_dt) + B3[j, j]*sqrt_dt)\
            * g(t+c[j]*dt, X)

        return x + a + b + diag - X

    @jit
    def fun_DAE(X, x, t, H, dt, xi_n, j):
        """
        define function handle to solve for case of SDAE
        :param X: place-holder for unknown
        :param x: value of last step
        :param t: value of time-step before
        :param H: saves already known internal stages
        :param dt: current size of time-step
        :param xi_n: step-size of Wiener Process/ Brownian Motion
        :param j: current index of H_j to compute
        :return: function to solve
        """
        sqrt_dt = np.sqrt(dt)
        a = np.zeros(n)
        b = np.zeros(n)
        for k in range(j):
            a += A[j, k] * dt * f(t+c[j]*dt, H[k, :])
            b += (B1[j, k]*xi_n + B2[j, k]*0.5*(xi_n**2-sqrt_dt) + B3[j, k]*sqrt_dt)\
                * g(t+c[j]*dt, H[k, :])

        diag = A[j, j] * dt * f(t+c[j]*dt, X) + \
            (B1[j, j]*xi_n + B2[j, j]*0.5*(xi_n**2-sqrt_dt) + B3[j, j]*sqrt_dt)\
            * g(t+c[j]*dt, X)

        return M.dot(x) + a + b + diag - M.dot(X)

    # implement different possibilities of SRK method

    # SDE explicit
    @jit
    def sde_explicit():
        """
        SRK method if Butcher-Tableau is explicit
        :return: approximated solution x
        """

        # iterate over all time-steps t
        for i in range(N - 1):
            dt = t[i + 1] - t[i]
            sqrt_dt = np.sqrt(dt)
            xi_n = np.random.normal(0, sqrt_dt)

            # iterate over all stages
            for j in range(s):
                H[j, :] = x[i, :]
                # get last H_s using explicit Butcher-tableau
                for k in range(j):
                    H[j, :] += A[j, k] * dt * f(t[i] + c[j] * dt, H[k, :]) \
                            + (B1[j, k] * xi_n + B2[j, k] * 0.5 * (xi_n ** 2 - sqrt_dt) + B3[j, k] * sqrt_dt) \
                            * g(t[i] + c[j] * dt, H[k, :])

            x[i + 1, :] = H[s - 1, :]

        return x

    # semi-explicit
    @jit
    def semi_explicit(fun_sol):
        """
        SRK method if only first stage of Butcher-Tableau is explicit
        :param fun_sol: information which pre-compiled function-handle should be used
        :return: approximated solution x
        """

        jac_inv = np.zeros((s, system_dimension, system_dimension))

        # iterating for every time-step
        for i in range(N - 1):
            dt = t[i + 1] - t[i]
            sqrt_dt = np.sqrt(dt)
            xi_n = np.random.normal(0, sqrt_dt)

            # set first stage
            H[0, :] = x[i, :]

            # iterate remaining stages
            for j in range(1, s):
                # define function for non-linear solver
                fun = lambda X: fun_sol(X, x[i, :], t[i], H, dt, xi_n, j)

                # solve non-linear problem
                H[j, :], jac_inv[j] = nb(fun, x[i, :], x_internal, r_internal, jac_inv[j])

            # set approximated step
            x[i + 1, :] = H[s - 1, :]

        return x

    # implicit
    @jit
    def implicit(fun_sol):
        """
        SRK method if Butcher-Tableau is implicit
        :param fun_sol: information which pre-compiled function-handle should be used
        :return: approximated solution x
        """

        # start iterating for all time-steps t
        for i in range(N - 1):
            dt = t[i + 1] - t[i]
            sqrt_dt = np.sqrt(dt)
            xi_n = np.random.normal(0, sqrt_dt)

            # iterate for all stages
            for j in range(s):
                # define function for non-linear solver
                fun = lambda X: fun_sol(X, x[i, :], t[i], H, dt, xi_n, j)

                # solve non-linear problem
                H[j, :] = nb(fun, x[i, :])

            # set approximated step
            x[i + 1, :] = H[s - 1, :]
        return x

    # SDE & SDAE switch semi-explicit/ implicit
    @jit
    def non_explicit(fun_sol):
        """
        differ cases of semi-explicit (explicit first stage) and diagonal implicit SRK method
        :param fun_sol: information which pre-compiled function-handle should be used
        :return: approximated solution x
        """
        # separate case: first stage is explicit
        if (butcher.A[0, 0] == 0) & (butcher.B3[0, 0] == 0):
            return semi_explicit(fun_sol)

        # all stages are implicit
        else:
            return implicit(fun_sol)

    # now start implementing SRK method

    # distinguish case of SDE and SDAE

    # SDE first
    if type == 'sde':

        # if Butcher-tableau is explicit
        if butcher.all_lower_triangular():
            x = sde_explicit()

        # else; Butcher-tableau implicit
        else:
            x = non_explicit(fun_ODE)

    # SDAE
    else:

        x = non_explicit(fun_DAE)

    return x


def f(t, x):
    return -np.sin(x)


def g(t, x):
    return 1


t = np.linspace(0, 10, 500)
x = stochastic_runge_kutta_method('sde', 0, f, g, 0, t, 0.)

plt.plot(t, x)
plt.show()
