from basics import *
import numpy as np


__author__ = 'marie'


'''
Class for creating and handling an extended Butcher-tableau for Stochastic-Runge-Kutta (SRK) method.

This type of Butcher-Tableau is of the form

 c | A | B1 | B2 | B3
 -------------------- .
   | a | b1 | b2 | b3

The Butcher-Tableau for SRK methods can be separated into 4 sub-matrices.
For SDAE they need to fulfill:
    - the first one A need to be invertible, except for the first row
    - the following two matrices B1 and B2 need to be explicit
    - the last one B3 need to be implicit, but does not need to be invertible.
For SDE they need to fulfill:
    - A is arbitrary
    - B1 and B2 need to be explicit
    - B3 is arbitrary again.
In both cases the order conditions as well as the consistency conditions need to be met.

For simplicity, set A, B1, B2, B3 manually, the lower-case variables are computed with the given sub-matrices
by calling 'set_tableau()'.



Example:

    butcher = Butcher(2)
    butcher.A = np.array([[1, 0], [0, 1]])
    butcher.B1 = np.array([[0, 0], [1, 0]])
    butcher.B2 = np.array([[0, 0], [1, 0]])
    butcher.B3 = np.array([[1, 0], [0, 1]])
    butcher.set_tableau()

'''


class Butcher(object):
    # initialize Butcher-tableau
    def __init__(self, s):
        """
        :param s: stages of Runge-Kutta method
        """
        # check for illegal arguments
        assert isinstance(s, int)

        # start setting values
        self.stages = s

        # getting the parts of Butcher-tableau
        self.c = np.array([s, 1])
        self.A = np.array([s, s])
        self.B1 = np.array([s, s])
        self.B2 = np.array([s, s])
        self.B3 = np.array([s, s])
        self.alpha = np.array([1, s])
        self.beta1 = np.array([1, s])
        self.beta2 = np.array([1, s])
        self.beta3 = np.array([1, s])

    # fill in missing entries of Butcher-tableau
    def set_tableau(self):
        """
        fills in the lower-case variables
        """
        e = np.ones(self.stages)

        self.c = self.A.dot(e)
        self.alpha = self.A[self.stages-1, :]
        self.beta1 = self.B1[self.stages-1, :]
        self.beta2 = self.B2[self.stages-1, :]
        self.beta3 = self.B3[self.stages-1, :]

    # check if tableau is valid, depending on guessed order
    def check(self, order):
        """
        :param order: assumed order of Runge-Kutta method, as float/double
        :return: True, if assumed order was correct, else return False
        """
        # check input data
        if not isinstance(order, float):
            raise TypeError

        e = np.ones(self.stages)
        # check if Butcher-tableau is valid
        if order == 0.5:
            # 1
            if not self.alpha.dot(e) == 1:
                return False
            # 2
            if not self.beta1.dot(e) == 1:
                return False
            # 3
            if not self.beta2.dot(e) == 0:
                return False
            # 4
            if not self.beta3.dot(e) == 0:
                return False
            # extra
            if not self.beta1.dot(self.B1.dot(e)) + 0.5*self.beta2.dot(self.B2.dot(e)) \
                    + self.beta3.dot(self.B3.dot(e)) == 0:
                return False

            return True

        elif order == 1.0:
            # 1
            if not self.alpha.dot(e) == 1:
                return False
            # 2
            if not self.beta1.dot(e) == 1:
                return False
            # 3
            if not self.beta2.dot(e) == 0:
                return False
            # 4
            if not self.beta3.dot(e) == 0:
                return False
            # 5 and getting lambda for further conditions
            lmbd = 2 * self.beta1.dot(self.B1.dot(e))
            # 6
            if not self.beta3.dot(self.B3.dot(e)) == -lmbd / 2:
                return False
            # 7
            if not self.beta2.dot(self.B3.dot(e)) + self.beta3.dot(self.B2.dot(e)) == 1-lmbd:
                return False
            # 8
            if not self.alpha.dot(self.B3.dot(e)) == 0:
                return False
            # 9
            if not self.beta1.dot(self.B3.dot(e)) + self.beta3.dot(self.B1.dot(e)) == 0:
                return False
            # 10
            if not self.beta2.dot(self.B2.dot(e)) == 0:
                return False
            # 11
            if not self.beta1.dot(self.B2.dot(e)) + self.beta2.dot(self.B1.dot(e)) == 0:
                return False
            # 12
            if not self.beta3.dot(self.A.dot(e)) == 0:
                return False
            # 13
            if not 2*self.beta1.dot(self.B1.dot(e)*self.B2.dot(e)) + 2*self.beta1.dot(self.B1.dot(e)*self.B3.dot(e))\
                    + self.beta2.dot(self.B1.dot(e)*self.B1.dot(e)) + self.beta2.dot(self.B2.dot(e)*self.B2.dot(e))\
                    + self.beta2.dot(self.B2.dot(e)*self.B3.dot(e)) + self.beta3.dot(self.B1.dot(e)*self.B1.dot(e))\
                    + 0.5*self.beta3.dot(self.B2.dot(e)*self.B2.dot(e)) + self.beta3.dot(self.B3.dot(e)*self.B3.dot(e))\
                    == 0:
                return False
            # 14
            if not self.beta1.dot(self.B1.dot(self.B2.dot(e))) + self.beta1.dot(self.B2.dot(self.B1.dot(e)))\
                    + self.beta1.dot(self.B1.dot(self.B3.dot(e))) + self.beta1.dot(self.B3.dot(self.B1.dot(e)))\
                    + self.beta2.dot(self.B1.dot(self.B1.dot(e))) + self.beta2.dot(self.B2.dot(self.B2.dot(e)))\
                    + 0.5*self.beta2.dot(self.B2.dot(self.B3.dot(e))) + 0.5*self.beta2.dot(self.B3.dot(self.B2.dot(e)))\
                    + self.beta3.dot(self.B1.dot(self.B1.dot(e))) + 0.5*self.beta3.dot(self.B2.dot(self.B2.dot(e)))\
                    + self.beta3.dot(self.B3.dot(self.B3.dot(e))) == 0:
                return False
            # 15
            if not (self.c == self.A.dot(e)).all():
                return False

            return True
        else:
            print('Butcher-Tableau unchecked; may not be valid')
            return True

    # check if condition of SDAE for sub-matrices are satisfied
    def check_condition_sdae(self):
        """
        check whether the Butcher-Tableau meets conditions for SDAE
        :return: True, if conditions are satisfied; False, otherwise
        """
        if strict_lower_triangular(self.B1) & strict_lower_triangular(self.B2) \
                & lower_triangular(self.B3) & (lower_triangular(self.A) & non_zero_diagonal(self.A[1:, 1:])):
            return True

        return False

    # check if condition of SDE for sub-matrices are satisfied
    def check_condition_sde(self):
        """
        check whether the Butcher-Tableau satisfies minimum conditions for SDE
        :return: True, if conditions are satisfied; False, otherwise
        """
        if strict_lower_triangular(self.B1) & strict_lower_triangular(self.B2):
            return True

        return False

    # check if given Butcher-tableau correspond to explicit method
    def all_lower_triangular(self):
        """
        check whether all sub-matrices of Butcher-Tableau are lower triangular, so explicit
        :return: True, if all sub-matrices are lower triangular; False, otherwise
        """
        return strict_lower_triangular(self.A) & strict_lower_triangular(self.B1) & strict_lower_triangular(self.B2) \
            & strict_lower_triangular(self.B3)
