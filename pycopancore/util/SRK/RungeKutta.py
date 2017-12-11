from .Butcher import *
import numpy as np
from .NewtonBroyden import newton_broyden as nb


__author__ = 'marie'


'''
Solver for Stochastic(-Algebraic) Differential Equations using concept of Stochastic-Runge-Kutta (SRK) methods.

Form of SDE
-----------
The SDE is assumed to be in shape of

dX = f(t, X)dt + g(t, X)dW,

where W is a stochastic process, to be more precise a Wiener Process. The stochastic variable X is assumed to be
time-dependant as well, but do not need to be.


Form of SDAE
------------
Analogously, the SDAE assumed to be in shape of

m_1 dX_D = f_D(t, X)dt + g(t, X)dW
m_2 dX_A = f_A(t, X)                ,

put together we get

M dX = f(t, X)dt + g(t, X)dW.

As suggested by the separated representation above there is assumed to be no noise in algebraic part.
Furthermore, it is needed that the left-hand side of the algebraic constraints can be transformed to 0
and f_A has a root (seriously, check it!!!).



The choice of Butcher-Tableau
------------------------------------------
For simplicity the choice of Butcher-Tableau is restricted to diagonal implicit cases.
If no Butcher-Tableau is given (give '0'), set a pre-defined order 1.0 SRK method.

The Butcher-Tableau for SRK methods is of the form

 c | A | B1 | B2 | B3
 --------------------
   | a | b1 | b2 | b3

the lower-case variables can be omitted by setting c = A e, where e = [1,...,1], and a = A_{s},
where A_{s} denotes the last row of A, same holds for B-matrices. For more information see documentation of
Butcher-class.

Note: for SDAE the sub-matrix A need to be invertible (or may have an explicit first stage with invertible sub-matrix);
      for SDE this conditions do not need to be met.

Furthermore, there are conditions for order 0.5 and 1.0 that are checked



Switching between different types of solver
-------------------------------------------
For selecting needed type of SRK method give 'sde' or 'sdae'.


'''


def stochastic_runge_kutta_method(type, M, f, g, butcher, t, x_0, reltol=1e-6, abstol=1e-8, force_full_compile=False):
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
    :param reltol: relative tolerance; default 1e-6
    :param abstol: absolute tolerance; default 1e-8
    :param force_full_compile: force full pre-compile

    :return: approximated solution x
    """

# do stuff before doing anything

    # assert right type of problem is inserted, else give hint
    assert type in ['sde', 'sdae'], "need to insert type of problem, 'sde' or 'sdae' "
    if type == 'sdae':
        if not len(x_0) == len(M):
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

    # save Jacobian-inverse of Newton-Broyden Method for later use
    app_jac_inv = [None] * s

    # reserve solution vector and a place-holder for internal steps
    H = np.zeros([s, n])
    x = np.zeros([N, n])
    x[0, :] = x_0

# ----------------------------------------------------------------------------------------------------------------------
# define pre-compiled functions for SRK

    # define pre-compiled function handles for later use
    # @jit(nopython=force_full_compile)
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

    # @jit(nopython=force_full_compile)
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

    # SDE explicit
    # @jit(nopython=force_full_compile)
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
    # @jit(nopython=force_full_compile)
    def semi_explicit(fun_sol):
        """
        SRK method if only first stage of Butcher-Tableau is explicit
        :param fun_sol: information which pre-compiled function-handle should be used
        :return: approximated solution x
        """
        # start with app_jac_inv=None, so do one step manually to get started
        dt = t[1] - t[0]
        sqrt_dt = np.sqrt(dt)
        xi_n = np.random.normal(0, sqrt_dt)
        H[0, :] = x[0, :]

        for j in range(1, s):
                # define function for non-linear solver
                fun = lambda X: fun_sol(X, x[i, :], t[i], H, dt, xi_n, j)

                # solve non-linear problem
                H[j, :], app_jac_inv[j] = nb(fun, x[0, :])

            # set approximated step
        x[1, :] = H[s - 1, :]

        # iterating for every time-step
        for i in range(1, N - 1):
            dt = t[i + 1] - t[i]
            sqrt_dt = np.sqrt(dt)
            xi_n = np.random.normal(0, sqrt_dt)

            # set first stage
            H[0, :] = x[i, :]

            # iterate remaining stages
            for j in range(1, s):
                # define function for non-linear solver
                fun = lambda X: fun_sol(X, x[0, :], t[0], H, dt, xi_n, j)

                # solve non-linear problem
                H[j, :], app_jac_inv[j] = nb(fun, x[i, :], jac_inv=app_jac_inv[j])

            # set approximated step
            x[i + 1, :] = H[s - 1, :]

        return x

    # implicit
    # @jit(nopython=force_full_compile)
    def implicit(fun_sol):
        """
        SRK method if Butcher-Tableau is implicit
        :param fun_sol: information which pre-compiled function-handle should be used
        :return: approximated solution x
        """
        dt = t[1] - t[0]
        sqrt_dt = np.sqrt(dt)
        xi_n = np.random.normal(0, sqrt_dt)

        # iterate for all stages
        for j in range(s):
            # define function for non-linear solver
            fun = lambda X: fun_sol(X, x[0, :], t[0], H, dt, xi_n, j)

            # solve non-linear problem
            H[j, :], app_jac_inv[j] = nb(fun, x[0, :])

        # set approximated step
        x[1, :] = H[s - 1, :]

        # start iterating for all time-steps t
        for i in range(1, N - 1):
            dt = t[i + 1] - t[i]
            sqrt_dt = np.sqrt(dt)
            xi_n = np.random.normal(0, sqrt_dt)

            # iterate for all stages
            for j in range(s):
                # define function for non-linear solver
                fun = lambda X: fun_sol(X, x[i, :], t[i], H, dt, xi_n, j)

                # solve non-linear problem
                H[j, :], app_jac_inv[j] = nb(fun, x[i, :], jac_inv=app_jac_inv[j])

            # set approximated step
            x[i + 1, :] = H[s - 1, :]
        return x

    # SDE & SDAE switch semi-explicit/ implicit
    # @jit(nopython=force_full_compile)
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


# ======================================================================================================================
# ----------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# test-example
#
# import matplotlib.pyplot as plt
#
# def f(t, x):
#     return -np.sin(x)
#
#
# def g(t, x):
#     return 1
#
#
# def main():
#     t = np.linspace(0, 1, 50)
#     x = stochastic_runge_kutta_method('sde', 0, f, g, 0, t, 0.5)
#
#     plt.plot(t, x)
#     plt.show()
#
#
# main()
