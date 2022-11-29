"""Enviroment process taxon mixing class template.

TODO: adjust, uncomment or fill in code and documentation wherever marked by
the "TODO" flag.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import interface as I
# from .... import master_data_model as D
# from ... import BBC_Biosphere as B
# TODO: uncomment this if you need ref. variables such as B.Environment.cells:
# from ...base import interface as B

# TODO: import those process types you need:
from pycopancore import ODE, Explicit, Event
import numpy as np


# import math

# def biological_pump(x,y):
#    I.Environment.bio_pump_strength=I.Environment.B_0*(1-I.Environment.B_T*x-I.Environment.B_TB*x)*(1-I.Environment.B_A*(
#                I.Environment.c_a0 * ((y / I.Environment.c_m0) ** I.Environment.r) * (1 / (1 - I.Environment.D_T * x)) - I.Environment.c_a0)

# def partial_pressure(x,y):
#    I.Environment.partial_pressure=I.Environment.c_a0*((x/I.Environment.c_m0)**I.Environment.r)*(1/(1-I.Environment.D_T-y))

class Environment(I.Environment):
    """Environment process taxon mixin implementation class."""

    # standard methods:
    # TODO: remove those that you don't use

    #def __init__(self,
    #               *,  # TODO: uncomment when adding named args after this
    #             **kwargs):
    #         """Initialize the unique instance of Environment."""
    #         super().__init__(**kwargs)  # must be the first line
    #         # TODO: add custom code here
    #         pass
    def __init__(self,
                 # *,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)

    # Functions
    def capacity_eqn(self, x, y, z):
        terrestrial_carbon_cap = (1 + self.K_c * np.log(z / self.c_a0)) * (np.max([np.exp(self.teta * np.log(1 - self.I_CC * np.abs(x - y))), 0])) * self.c_t0 / self.Q_R ** (
                                                  x / 10) - self.K_A * np.abs(x - y)
        return terrestrial_carbon_cap

    def productivity_eqn(self, x, y):
        product = np.max([np.exp(self.teta*np.log(1-self.I_CC*np.abs(x-y))), 0])
        return product

    def pressure_eqn(self, x, y):
        partial_pressure = self.c_a0 * ((y / self.c_m0) ** self.r) / (1 - self.D_T * x)
        return partial_pressure

    def pump_eqn(self, x, y):
        bio_pump_strength = self.B_0 * (1 - self.B_T * x - self.B_TB * x) * (1 - self.B_A * (self.pressure_eqn(x, y) - self.c_a0))
        return bio_pump_strength

    # ODEs
    def temperature_eqn(self, t):
        self.d_temperature = (self.lam * np.log(self.carbon_atmosphere/self.c_a0) / np.log(2) - self.temperature) / self.tau

    def get_temperature_slope(self, t):
        self.temperature_slope = (self.lam * np.log(self.carbon_atmosphere/self.c_a0) / np.log(2) - self.temperature) / self.tau

    def response_lag_eqn(self, t):
        self.d_response_lag=self.productivity_eqn(self.temperature, self.response_lag)*np.tanh(self.r_g*(self.temperature-self.response_lag)/self.v_max)*self.v_max
        #self.d_response_lag += max((np.exp(self.teta * np.log(1 - self.I_CC * np.abs(self.temperature - self.response_lag)))), 0) * np.tanh(
        #    self.r_g * (self.temperature - self.response_lag) / self.v_max) * self.v_max

    def terrestrial_carbon_eqn(self, t):
        self.d_carbon_terrestial += (self.NPP/self.c_t0) * (
                    self.Q_R ** (self.temperature / 10)) * (self.capacity_eqn(self.temperature, self.response_lag, self.carbon_atmosphere)-self.carbon_terrestial)-self.LUC

    def marine_carbon_eqn(self, t):
        # print(self.carbon_mixed_laxer)
        self.d_carbon_mixed_laxer += self.Dd/(self.pressure_eqn(0, self.c_m0)*self.r/self.c_m0)*((self.carbon_atmosphere*(1-self.dis)+self.c_a0*self.dis)-self.pressure_eqn(self.temperature, self.carbon_mixed_laxer))-(self.pump_eqn(self.temperature, self.carbon_mixed_laxer)-self.pump_eqn(0, self.c_m0))-self.w_0*(1-self.w_T*self.temperature)*(self.carbon_mixed_laxer-self.c_m0)
        #self.d_carbon_mixed_laxer += ((self.Dd*self.c_m0)/(self.c_a0*self.r))*\
        #                             (self.carbon_atmosphere -(self.c_a0*((self.carbon_mixed_laxer/self.c_m0)**self.r)/
        #                                                                        (1-(self.D_T*self.temperature))))-self.B_0-\
        #                            (self.B_0*(1-self.B_T*self.temperature-self.B_TB*self.temperature))*\
        #                            (1-self.B_A*((self.carbon_atmosphere*((self.carbon_mixed_laxer/self.c_m0)**self.r)
        #                                           /(1-(self.D_T*self.temperature)))-self.c_a0))-self.w_0*(1-self.w_T*self.temperature)\
        #                            *(self.carbon_mixed_laxer-self.c_m0)
        #self.d_carbon_mixed_laxer += self.carbon_mixed_laxer

    def carbon_system_eqn(self, t):
        self.d_carbon_system += self.e - (self.B_0 * (1 - self.B_T * self.temperature - self.B_TB * self.temperature) * (1 - self.B_A * (self.c_a0 * ((self.carbon_mixed_laxer / self.c_m0) ** self.r) / (1 - self.D_T * self.temperature)) - self.c_a0))-self.B_0-self.w_0*(1-self.w_T*self.temperature)*(self.carbon_mixed_laxer-self.c_m0)

    def perma_warming_eqn(self, t):
        self.d_perma_tenperature += max(self.temperature_slope, 0)

    # #Explicit
    def atmosphere_carbon(self, t):
        self.carbon_atmosphere = self.c_a0+self.c_t0+self.c_m0+(self.p_T*self.perma_tenperature)+self.carbon_system-self.carbon_mixed_laxer-self.carbon_terrestial

    # random event
    #def event(self, t):
     #   self.dummy_variable = 0
    #    print("I did an event!\n")

    #def event_time(self, t):
    #    return t + 1

    processes = [
        ODE("global warming", [I.Environment.temperature], temperature_eqn),
        Explicit("temperature slope", [I.Environment.temperature_slope], get_temperature_slope),
        ODE("response lag of the biosphere", [I.Environment.response_lag], response_lag_eqn),
        ODE("terrestrial carbon", [I.Environment.carbon_terrestial], terrestrial_carbon_eqn),
        ODE("marine carbon", [I.Environment.carbon_mixed_laxer], marine_carbon_eqn),
        ODE("system carbon", [I.Environment.carbon_system], carbon_system_eqn),
        Explicit("atmospheric carbon", [I.Environment.carbon_atmosphere], atmosphere_carbon),
        ODE("permafrost melting", [I.Environment.perma_tenperature], perma_warming_eqn)
        #Event("event", [I.Environment.dummy_variable], ["time"])
                 ]


    # def terrestrial_emmitting(self, t):
    #    """Calculating the emissions from permaforst melting"""
    #    self.terrestrial_carbon_cap = (self.productivity * (
    ##           (1 + self.K_c * np.log(self.carbon_atmosphere / self.c_a0)) / self.Q_R ** (
    #           self.temperature / 10)) * self.c_t0) - self.K_A * np.absolute(
    #       self.temperature - self.response_lag)
    #   self.d_carbon_terrestial += (self.NPP / self.c_t0) * self.Q_R ** (self.temperature / 10) * (
    #           self.terrestrial_carbon_cap - self.carbon_terrestial) - self.LUC

    #    def biological_pump(self, x, y):
    #        self.bio_pump_strength = self.B_0 * (1 - self.B_T * x - self.B_TB * x) * (
    #                    1 - self.B_A * (
    #                    self.c_a0 * ((y / I.Environment.c_m0) ** I.Environment.r) * (
    #                       1 / (1 - self.D_T * x)) - self.c_a0)

    #    def partial_pressure(self, x, y):
    #        self.partial_pressure = self.c_a0 * ((x / self.c_m0) ** self.r) * (
    #                    1 / (1 - self.D_T - y))

    # def biological_pump(self, t):
    #     """calculating the emissions from the mixed layer"""
    #     self.cabon_mixed_laxer += (self.Dd * self.c_m0 / (self.c_a0 * self.r)) - self.B_0 \
    #                             - (self.B_0 * (1 - self.B_T * self.temperature - self.B_TB * self.temperature) * (
    #            1 - self.B_A * (self.c_a0 * ((self.cabon_mixed_laxer / self.c_m0) ** self.r) * (
    #            1 / (1 - self.D_T * self.temperature)) - self.c_a0))) \
    #                            - self.w_0 * (1 - self.w_T * self.temperature) * (self.cabon_mixed_laxer - self.c_m0)

    #        F_1=((D*c_m0)/(c_a0**r))*(self.carbon_atmosphere-(c_a0(self.cabon_mixed_laxer/c_m0)**r))*(1/(1-D_T*self.temperature))
    #        F_2=(B_0*(1-B_T*self.temperature-B_TB*self.temperature))*(1-B_A((c_a0*(self.cabon_mixed_laxer/c_m0)**r)*(1/(1-D_T*self.temperature))-c_a0))
    # self.d_cabon_mixed_laxer+=(((self.Dd*self.c_m0)/(self.c_a0**self.r))*(self.carbon_atmosphere-(self.c_a0*(self.cabon_mixed_laxer/self.c_m0)**self.r))*(1/(1-self.D_T*self.temperature)))-(self.B_0*(1-self.B_T*self.temperature-self.B_TB*self.temperature))*(1-self.B_A*((self.c_a0*(self.cabon_mixed_laxer/self.c_m0)**self.r)*(1/(1-self.D_T*self.temperature))-self.c_a0))-(self.B_0*(self.B_T*(self.c_a0**self.r)))-self.w_0*(1-self.w_T*self.temperature)*(self.cabon_mixed_laxer*self.c_m0)

    # def total_cabon_emissions(self, t):
    #   """calculating the cumulated system carbon"""
    #   #        F_3=(B_0*(1-B_T*self.temperature-B_TB*self.temperature))*(1-B_A((c_a0*(self.cabon_mixed_laxer/c_m0)**r)*(1/(1-D_T*self.temperature))-c_a0))
    #   self.carbon_atmosphere = self.c_a0 + self.c_t0 + self.c_m0 + self.carbon_system + self.perma_carbon + self.carbon_terrestial + self.cabon_mixed_laxer
    #   self.d_carbon_system += self.e - (
    #               (self.B_0 * (1 - self.B_T * self.temperature - self.B_TB * self.temperature) * (
    #                       1 - self.B_A * (self.c_a0 * ((self.cabon_mixed_laxer / self.c_m0) ** self.r) * (
    #                       1 / (1 - self.D_T * self.temperature)) - self.c_a0))) - self.B_0) - (
    #                                      self.w_0 * (1 - self.w_T * self.temperature) * (
    #                                          self.cabon_mixed_laxer - self.c_m0))

    # def warming(self, t):
    #    """calculating the warming rate"""
    #    self.d_temperature += (1 / self.tau) * (
    #        (self.lam / (np.log(2)) * (np.log(self.carbon_atmosphere / self.c_a0)) - self.temperature))

    # def response(self, t):
    #    """Calculating the response lag of the biosphere"""
    #    # self.measurre_biodiv=1-self.I_CC*np.absolute(self.temperature-self.response_lag)-self.I_d
    #    self.measurre_biodiv = 1
    #    self.productivity = np.max(np.exp(self.teta * np.log(self.measurre_biodiv)), 0)
    #   self.d_response_lag += self.v_max * self.productivity * np.tanh(
    #        (self.r_g * (self.temperature - self.response_lag)) / self.v_max)

    # def perma_melting(self, t):
    #     """Calculating the emissions from permaforst melting"""
    #     self.d_perma_tenperature += np.absolute(self.temperature)
    #     self.perma_carbon = self.p_T * self.perma_tenperature

    # processes=[ODE("emissions from terra", [I.Environment.terrestrial_carbon_cap, I.Environment.carbon_terrestial], terrestrial_emmitting),
    # ODE("emissions from mixed layer",[I.Environment.cabon_mixed_laxer],[biological_pump]),
    # ODE("total emissions",[I.Environment.carbon_atmosphere, I.Environment.carbon_system],[total_cabon_emissions]),
    # ODE("temperature rise", [I.Environment.temperature],[warming]),
    # ODE("resonse lag",[I.Environment.measurre_biodiv, I.Environment.productivity, I.Environment.response_lag],response),
    #              ODE("permafrost melting", [I.Environment.perma_tenperature, I.Environment.perma_carbon],perma_melting)]  # TODO: instantiate and list process objects here
    #processes = [ODE("emissions from terra", [I.Environment.carbon_terrestial], terrestrial_emmitting),
    #             ODE("emissions from mixed layer", [I.Environment.carbon_mixed_laxer], biological_pump),
    #             ODE("total emissions", [I.Environment.carbon_system], total_cabon_emissions),
    #             ODE("temperature rise", [I.Environment.temperature], warming),
     #            ODE("resonse lag", [I.Environment.response_lag], response),
     #            ODE("permafrost melting", [I.Environment.perma_tenperature], perma_melting)]
