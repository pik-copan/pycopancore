from .interface import * # import all interface classes since one typically wants to cross-ref variables between entity types (this is the whole point of having an interface in the first place)
from pycopancore.model_components import abstract


class Cell(Cell_, abstract.Cell):
    """
    """

    # standard methods:

    def __init__(self,
                 *,
                 terrestrial_carbon = 1,
                 **kwargs
                 ):
        """Initialize a cell"""
        super().__init__(**kwargs)
        # initial values:
        self.terrestrial_carbon = terrestrial_carbon


    # process-related methods:
    
    def do_photosynthesis(self, unused_t):
        """compute and store rhs of ODE photosynthesis"""

        # abbreviations:
        L = self.terrestrial_carbon
        Sigma = self.land_area
        
        self.photosynthesis_flow = ((Nature_.basic_photosynthesis_productivity 
                                     - Nature_.photosynthesis_temperature_sensitivity * self.world.mean_surface_air_temperature)
                                    * sqrt(self.world.atmospheric_carbon / Sigma)
                                    * (1 - L / (Nature_.terrestrial_carbon_capacity_per_area * Sigma))) \
                                * L
        
        self.d_terrestrial_carbon += self.photosynthesis_flow

    def do_respiration(self, t):
        """compute and store rhs of ODE respiration"""
       
        self.respiration_flow = (Nature_.basic_respiration_rate 
                                 + Nature_.respiration_temperature_sensitivity * self.world.mean_surface_air_temperature) \
                             * self.terrestrial_carbon
        
        self.d_terrestrial_carbon += - self.respiration_flow


    processes = [
                 # example with argument names:
                 ODE(name="photosynthesis", variables=[Cell.terrestrial_carbon], specification=do_photosynthesis),
                 # example without:
                 ODE("respiration", [Cell.terrestrial_carbon], do_respiration),
                 # alternatively later when symbolic expressions are enabled:
#                  Explicit("flows", [Cell.photosynthesis_flow, Cell.respiration_flow], [
#                             ((Nature_.basic_photosynthesis_productivity 
#                                      - Nature_.photosynthesis_temperature_sensitivity * Cell.world.mean_surface_air_temperature)
#                                     * sqrt(Cell.world.atmospheric_carbon / Cell.land_area)
#                                     * (1 - Cell.terrestrial_carbon / (Nature_.terrestrial_carbon_capacity_per_area * Cell.land_area)))
#                             * Cell.terrestrial_carbon,
#                             (Nature_.basic_respiration_rate 
#                                  + Nature_.respiration_temperature_sensitivity * Cell.world.mean_surface_air_temperature)
#                             * Cell.terrestrial_carbon
#                         ]),
#                  ODE("changes", [Cell.terrestrial_carbon], [
#                             Cell.photosynthesis_flow - Cell.respiration_flow
#                         ]),
                 ]

        