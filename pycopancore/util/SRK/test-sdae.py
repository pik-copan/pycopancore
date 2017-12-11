import numpy as np
import RungeKutta as rk
import matplotlib.pyplot as plt


__author__ = 'marie'

'''
treat system:
      dot(phi_1) = omega_1
      dot(phi_2) = omega_2
H_1 dot(omega_1) = -alpha_1 omega_1 + P_1 - Re(U_1 I_1^H) + E_1
H_2 dot(omega_2) = -alpha_2 omega_2 + P_2 - Re(U_2 I_2^H)
        dot(E_1) = g E_1 - E_1^2 / E_0 + sqrt(D) |E_1| Y_1
        dot(Y_1) = -gamma Y_1                                   + Gamma
               0 = Q_1 - Im(U_1 I_1^H)
               0 = Q_2 - Im(U_2 I_2^H)

'''


def main(x_0, n):

    """
    :param x_0: initial value
    :param n: number of nodes
    """

    def f(t, x):
        alpha = np.array([1, 0])
        p = np.array([complex(1, x[6]), complex(-1, -1)])
        gamma = 1.
        e0 = .1
        D = 1.
        G = .75

        ui = np.zeros(n, dtype=np.complex128)
        v = np.array([1, x[7]])
        y = 10. * np.array([[1, -1], [-1, 1]])
        for i in range(n):
            for j in range(n):
                ui[i] += v[i] * v[j].conjugate() * y[i, j].conjugate() * np.exp(1.j * (x[i]-x[j]))

        value = np.empty(8, dtype=np.float64)

        value[0] = x[2]
        value[1] = x[3]
        value[2] = -alpha[0] * x[2] + np.real(p[0]) - np.real(ui[0]) + x[4]
        value[3] = -alpha[1] * x[3] + np.real(p[1]) - np.real(ui[1])
        value[4] = G * x[4] - 1/e0 * x[4]**2 + np.sqrt(D) * np.abs(x[4]) * x[5]
        value[5] = -gamma * x[5]
        value[6] = np.imag(p[0]) - np.imag(ui[0])
        value[7] = np.imag(p[1]) - np.imag(ui[1])

        return value

    def g(t, x):
        value = np.empty(8)
        value[5] = .2
        return value

    H = np.ones(n)

    M = np.diag(np.ones(8, dtype=np.float64))
    M[2, 2] = H[0]
    M[3, 3] = H[1]
    M[-1, -1] = 0
    M[-2, -2] = 0

    t = np.linspace(0, .25, 150)

    x = rk.stochastic_runge_kutta_method('sdae', M, f, g, 0, t, x_0)

    plt.plot(t, x)
    plt.show()

    np.save("states", x)

    return 0

x_0 = np.ones(8) * 0.5
x_0[0] = 0.
main(x_0, 2)
