from .interface import * # import all interface classes since one typically wants to cross-ref variables between entity types (this is the whole point of having an interface in the first place)
from pycopancore.model_components import abstract

class Cell(Cell_, abstract.Cell):
    """
    """

    # attributes:
    
    processes = [
                 ODE(name="natural_vegetation_dynamics", variables=[terrestrial_carbon], specification=do_natural_vegetation_dynamics),
                 ]


    # standard methods:

    def __init__(self,
                 # ,*,
                 **kwargs):
        """Initialize a cell"""
        super().__init__(**kwargs)
        # add custom code here:
        pass


    # process-related methods:
    
    def do_natural_vegetation_dynamics(self, t):
        """compute and store rhs of ODE natural_vegetation_dynamics"""

        # abbreviations:
        L = self.terrestrial_carbon
        T = self.world.mean_surface_air_temperature
        Sigma = self.land_area
        
        # rates:
        photosynthesis_rate = (Nature_.basic_photosynthesis_productivity - Nature_.photosynthesis_temperature_sensitivity * T) \
            * sqrt(self.world.atmospheric_carbon / Sigma) \
            * (1 - L / (Nature_.terrestrial_carbon_capacity_per_area * Sigma))
        respiration_rate = Nature_.basic_respiration_rate + Nature_.respiration_temperature_sensitivity * T
        
        self.d_terrestrial_carbon = (photosynthesis_rate - respiration_rate) * L
        