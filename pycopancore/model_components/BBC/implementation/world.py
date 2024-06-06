
# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license
from ... import abstract
from .. import interface as I

# TODO: uncomment this if you need ref. variables such as B.World.cells:
from ...base import interface as B

# TODO: import those process types you need:
from .... import Explicit, ODE, Event
import numpy as np


class World(I.World):

    # Functions
    def capacity_eqn(self, T, z, ca):
        """Function for calculating the terrestrial carbon carrying capacity depending on Temperature T, response lag z
        and atmospheric carbon ca."""
        terrestrial_carbon_cap = (1 + self.environment.K_c * np.log(
            ca / self.environment.c_a0)) * self.productivity_eqn(self.environment.temperature,
                                                                 self.environment.response_lag) * self.environment.c_t0 / (
                                         self.environment.Q_R ** (
                                         T / 10)) - self.environment.K_A * np.abs(T - z)
        return terrestrial_carbon_cap

    def productivity_eqn(self, T, z):
        """Function for calculating the biosphere productivity depending on the Temperature T and the response lag z"""
        product = max([np.exp(
            self.environment.teta * np.log(1 - self.environment.I_CC * np.abs(T - z))), 0])
        return product

    def pressure_eqn(self, T, cm):
        """Function for calculating the partial pressure of CO2 in the ocean, depending on the Temperature T and
        the mixed layer carbon cm"""
        partial_pressure = self.environment.c_a0 * ((cm / self.environment.c_m0) ** self.environment.r) / (
                    1 - self.environment.D_T * T)
        return partial_pressure

    def pump_eqn(self, T, cm):
        """Function for calculating the strength of the biological pump (in the ocean) depending on the Temperature T
        and the mixed layer carbon cm"""
        bio_pump_strength = self.environment.B_0 * (1 - self.environment.B_T * T - self.environment.B_TB * T) * (
                1 - self.environment.B_A * (self.pressure_eqn(T, cm) - self.environment.c_a0) / 2.134)
        return bio_pump_strength

    # ODEs
    def temperature_eqn(self, t):
        """ODE for calculating the global mean temperature T"""
        self.environment.d_temperature += (self.environment.lam * np.log(
            self.environment.carbon_atmosphere / self.environment.c_a0) / np.log(
            2) - self.environment.temperature) / self.environment.tau
        # print("this is T:", self.temperature)

    def biodiv_eqn(self, t):
        """Function to update the global measure for biodiversity J."""
        if t < 2000:
            self.environment.J = 1 - self.environment.I_CC * np.abs(
                self.environment.temperature - self.environment.response_lag) - self.metabolism.J_d
        else:
            self.environment.J = 1 - self.environment.I_CC * np.abs(
                self.environment.temperature - self.environment.response_lag) - self.metabolism.J_d_new

    def get_temperature_slope(self, unused_t):
        """Explicit function for calculating the slope of the global mean temperature """
        self.environment.temperature_slope = ((np.log(
            self.environment.carbon_atmosphere / self.environment.c_a0) * self.environment.lam / np.log(
            2)) - self.environment.temperature) / self.environment.tau

    def response_lag_eqn(self, t):
        """ODE fo calculating the biosphere response lag """
        self.environment.d_response_lag += self.productivity_eqn(self.environment.temperature,
                                                                 self.environment.response_lag) * \
                                           np.tanh(self.environment.r_g * (
                                                       self.environment.temperature - self.environment.response_lag) / self.environment.v_max) * self.environment.v_max

    def terrestrial_carbon_eqn(self, t):
        """ODE for calculating the terrestrial carbon"""
        self.environment.d_carbon_terrestrial += (self.environment.NPP / self.environment.c_t0) * (
                    self.environment.Q_R ** (self.environment.temperature / 10)) * \
                                                (self.capacity_eqn(self.environment.temperature,
                                                                   self.environment.response_lag,
                                                                   self.environment.carbon_atmosphere) -
                                                 self.environment.carbon_terrestrial) - self.metabolism.LUC

    def marine_carbon_eqn(self, t):
        """ODE for calculating the mixed layer carbon"""
        self.environment.d_carbon_mixed_laxer += self.environment.Dd / (
                    self.pressure_eqn(0, self.environment.c_m0) * self.environment.r / self.environment.c_m0) * (
                                                         self.environment.carbon_atmosphere - self.pressure_eqn(
                                                     self.environment.temperature, self.environment.carbon_mixed_laxer))
        - self.pump_eqn(self.environment.temperature, self.environment.carbon_mixed_laxer) - self.pump_eqn(0,
                                                                                                           self.environment.c_m0) - self.environment.w_0 * \
        (self.environment.w_T * self.environment.temperature) * (
                    self.environment.carbon_mixed_laxer - self.environment.c_m0)

    def carbon_system_eqn(self, t):
        """ODE fo calculating the carbon within the whole system"""
        self.environment.d_carbon_system += self.metabolism.e_new - self.environment.w_0 * (
                    1 - self.environment.w_T * self.environment.temperature) * (
                                                    self.environment.carbon_mixed_laxer - self.environment.c_m0) - \
                                            (self.pump_eqn(self.environment.temperature,
                                                           self.environment.carbon_mixed_laxer) - self.pump_eqn(0,
                                                                                                                self.environment.c_m0))

    def perma_warming_eqn(self, t):
        """ODE for calculating the temperature of permafrost"""
        self.environment.d_perma_temperature += max([self.environment.temperature_slope, 0])

    # Explicit Functions
    def atmosphere_carbon(self, unused_t):
        """Explicit Function for calculating the atmospheric carbon"""
        self.environment.carbon_atmosphere = self.environment.c_a0 + self.environment.c_t0 + self.environment.c_m0 + (
                self.environment.p_T * self.environment.perma_temperature) + self.environment.carbon_system - self.environment.carbon_mixed_laxer - self.environment.carbon_terrestrial

    def behavioural_decision_CC(self, t):
        """Explicit Functions for calculating the behavioural decisions referred to climate change, the function for
            calculating the perceived risk can be linear, cubic or logistic and the implementation of the Theory of
            Planed Behaviour can be linear and multiplied"""
        if t < 2000:
            self.culture.behavioural_change_BD = 0
        else:
            if self.culture.PR == 1: #linear
                self.culture.perceived_risk_CC = (2 / 3) * self.environment.temperature - 1
            if self.culture.PR == 2: #logistic
                self.culture.perceived_risk_CC = 2 / (1 + np.exp(-4.5 * (self.environment.temperature - 1.5))) - 1
            if self.culture.PR == 3: #cubic
                self.culture.perceived_risk_CC = (8 / 27) * (self.environment.temperature - 1.5) ** 3
            if self.culture.PR == 4: #convex
                self.culture.perceived_risk_CC = ((2 / 27) * self.environment.temperature ** 3) - 1
            if self.culture.PR == 5: #concave
                self.culture.perceived_risk_CC = ((2 / 27) * (self.environment.temperature - 3) ** 3) + 1

            if self.culture.TPB == 1: #multiplied
                self.culture.attitude_CC = self.culture.alp * ((self.culture.Ef_CC ** (self.culture.w1 + 0.5)) * (
                            np.abs(self.culture.perceived_risk_CC) ** ((1 - self.culture.w1) + 0.5)))
                if self.culture.perceived_risk_CC < 0:
                    self.culture.attitude_CC = self.culture.attitude_CC * (-1)
                self.culture.behavioural_intention_CC = (self.culture.wA * self.culture.attitude_CC) + (
                            (1 - self.culture.wA) * self.culture.SN_CC)
                self.culture.behavioural_change_CC = (np.abs(self.culture.behavioural_intention_CC) ** (
                            self.culture.w2 + 0.5)) * (((0.5 * self.culture.PBC_CC) + 0.5) ** (
                            (1 - self.culture.w2) + 0.5))
                if self.culture.behavioural_intention_CC < 0:
                    self.culture.behavioural_change_CC = self.culture.behavioural_change_CC * (-1)
            if self.culture.TPB == 2: #linear
                self.culture.attitude_CC = self.culture.alp * ((self.culture.Ef_CC ** (self.culture.w1 + 0.5)) * (
                            np.abs(self.culture.perceived_risk_CC) ** ((1 - self.culture.w1) + 0.5)))
                if self.culture.perceived_risk_CC < 0:
                    self.culture.attitude_CC = self.culture.attitude_CC * (-1)
                self.culture.behavioural_intention_CC = ((self.culture.wA * self.culture.attitude_CC) + (
                            self.culture.wN * self.culture.SN_CC) + (self.culture.wC * self.culture.PBC_CC)) * (1 / (
                            self.culture.wA + self.culture.wN + self.culture.wC))
                self.culture.behavioural_change_CC = (self.culture.w2 * self.culture.behavioural_intention_CC) + (
                            (1 - self.culture.w2) * self.culture.PBC_CC)  # linear TBH

    def behavioural_decision_BD(self, t):
        """Explicit Functions for calculating the behavioural decisions referred to climate change, the function for
            calculating the perceived risk can be linear, cubic or logistic and the implementation of the Theory of
            Planed Behaviour can be linear and multiplied"""
        if t < 2000:
            self.culture.behavioural_change_BD = 0
        else:
            if self.culture.PR == 1:  # linear
                self.culture.perceived_risk_BD = (-2) * self.environment.J + 1
            if self.culture.PR == 2:  # logistic
                self.culture.perceived_risk_BD = 2 / (1 + np.exp(12 * (self.environment.J - 0.5))) - 1
            if self.culture.PR == 3:  # cubic
                self.culture.perceived_risk_BD = (-8) * (self.environment.J - 0.5) ** 3
            if self.culture.PR == 4:  # convex
                self.culture.perceived_risk_BD = ((-2) * (self.environment.J - 1) ** 3) - 1
            if self.culture.PR == 5:  # concave
                self.culture.perceived_risk_BD = ((-2) * (self.environment.J ** 3)) + 1

            if self.culture.TPB == 1:  # multiplied
                self.culture.attitude_BD = (1 - self.culture.alp) * ((self.culture.Ef_BD ** (self.culture.w1 + 0.5)) * (
                            np.abs(self.culture.perceived_risk_BD) ** ((1 - self.culture.w1) + 0.5)))
                if self.culture.perceived_risk_BD < 0:
                    self.culture.attitude_BD = self.culture.attitude_BD * (-1)
                self.culture.behavioural_intention_BD = (self.culture.wA * self.culture.attitude_BD) + (
                            (1 - self.culture.wA) * self.culture.SN_BD)
                self.culture.behavioural_change_BD = (np.abs(self.culture.behavioural_intention_BD) ** (
                            self.culture.w2 + 0.5)) * (((0.5 * self.culture.PBC_BD) + 0.5) ** (
                            (1 - self.culture.w2) + 0.5))
                if self.culture.behavioural_intention_BD < 0:
                    self.culture.behavioural_change_BD = self.culture.behavioural_change_BD * (-1)
            if self.culture.TPB == 2:  # linear
                self.culture.attitude_BD = (1 - self.culture.alp) * ((self.culture.Ef_BD ** (self.culture.w1 + 0.5)) * (
                            np.abs(self.culture.perceived_risk_BD) ** ((1 - self.culture.w1) + 0.5)))
                if self.culture.perceived_risk_BD < 0:
                    self.culture.attitude_BD = self.culture.attitude_BD * (-1)
                self.culture.behavioural_intention_BD = ((self.culture.wA * self.culture.attitude_BD) + (
                            self.culture.wN * self.culture.SN_BD) + (self.culture.wC * self.culture.PBC_BD)) * (1 / (
                            self.culture.wA + self.culture.wN + self.culture.wC))
                self.culture.behavioural_change_BD = (self.culture.w2 * self.culture.behavioural_intention_BD) + (
                            (1 - self.culture.w2) * self.culture.PBC_BD)

    def update_time(self, t):
        """Event that counts the years t"""
        return t + 1

    def update_1(self, t):
        """Event foc calculation the response rates can be cummulative or not"""
        self.metabolism.max_change_CC = (self.metabolism.e - self.metabolism.e_min) * self.metabolism.R_max_CC
        if t < 2000:
            self.metabolism.cum_CC = 0
        else:
            self.metabolism.cum_CC = (self.culture.behavioural_change_CC * self.metabolism.max_change_CC)

        self.metabolism.max_change_BD = (self.metabolism.J_d - self.metabolism.i_min) * self.metabolism.R_max_BD
        if t < 2000:
            self.metabolism.cum_BD = 0
        else:
            self.metabolism.cum_BD = (self.culture.behavioural_change_BD * self.metabolism.max_change_BD)

    def mitigation_CC(self, t):
        """Explicit Functions for calculating the behaviour dependend Emissions e """
        if t < 2000:
            self.metabolism.e_new = self.metabolism.e
        else:
            self.metabolism.e_new = self.metabolism.e - self.metabolism.cum_CC

    def mitigation_BD(self, t):
        """Explicit Functions for calculating the behaviour dependend Human Impact on the biosphere J_d """
        if t < 2000:
            self.metabolism.J_d_new = self.metabolism.J_d
        else:
            self.metabolism.J_d_new = self.metabolism.J_d - self.metabolism.cum_BD

    def update(self, t):
        """Event for updating the Emissions e, the Land-use-change LUC and the Measure for Biodiversity J """
        print(t)
        self.metabolism.e = self.metabolism.emission_array[t - 1765][1]
        self.metabolism.LUC = self.metabolism.LUC_array[t - 1765][1]
        self.metabolism.J_d = 0.1 * min((t - 1765) / (2000 - 1765), 1) + 0.18 * max(0, (t - 2000) / (2100 - 2000))

    processes = [
        Event("update e and Id und LUC", [B.World.metabolism.e, B.World.metabolism.LUC, B.World.metabolism.J_d],
              ["time", update_time, update]),
        Explicit("biodiversity update", [B.World.environment.J], biodiv_eqn),
        ODE("global warming", [B.World.environment.temperature], temperature_eqn),
        Explicit("temperature slope", [B.World.environment.temperature_slope], get_temperature_slope),
        ODE("response lag of the biosphere", [B.World.environment.response_lag], response_lag_eqn),
        ODE("terrestrial carbon", [B.World.environment.carbon_terrestrial], terrestrial_carbon_eqn),
        ODE("marine carbon", [B.World.environment.carbon_mixed_laxer], marine_carbon_eqn),
        ODE("system carbon", [B.World.environment.carbon_system], carbon_system_eqn),
        Explicit("atmospheric carbon", [B.World.environment.carbon_atmosphere], atmosphere_carbon),
        ODE("permafrost melting", [B.World.environment.perma_temperature], perma_warming_eqn),
        Explicit("behavioural decision CC", [
            B.World.culture.SN_CC, B.World.culture.PBC_CC,
            B.World.culture.perceived_risk_CC, B.World.culture.attitude_CC,
            B.World.culture.behavioural_change_CC, B.World.culture.behavioural_intention_CC], behavioural_decision_CC),
        Explicit("behavioural decision BD", [
            B.World.culture.SN_BD, B.World.culture.PBC_BD,
            B.World.culture.perceived_risk_BD, B.World.culture.attitude_BD, B.World.culture.behavioural_intention_BD,
            B.World.culture.behavioural_change_BD,
        ], behavioural_decision_BD),
        Event("cum", [B.World.metabolism.max_change_CC, B.World.metabolism.cum_CC, B.World.metabolism.max_change_BD,
                      B.World.metabolism.cum_BD], ["time", update_time, update_1]),
        Explicit("mitigation climate change", [B.World.metabolism.e_new], mitigation_CC),
        Explicit("mitigation biodiv change", [B.World.metabolism.J_d_new], mitigation_BD),
    ]
