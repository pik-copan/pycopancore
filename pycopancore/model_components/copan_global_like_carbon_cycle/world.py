from .interface import * # import all interface classes since one typically wants to cross-ref variables between entity types (this is the whole point of having an interface in the first place)
from pycopancore.model_components import abstract


class World (World_, abstract.World):
    """
    """

    
    # standard methods:    

    def __init__(self,
                 *,
                 atmospheric_carbon = 1,
                 upper_ocean_carbon = 1,
                 mean_surface_air_temperature = 0,
                 **kwargs
                 ):
        """Initialize an (typically the unique) instance of World."""
        super().__init__(**kwargs)
        # initial values:
        self.atmospheric_carbon = atmospheric_carbon
        self.upper_ocean_carbon = upper_ocean_carbon
        self.mean_surface_air_temperature = mean_surface_air_temperature
        
        
    # process-related methods:
    
    def aggregate_stocks(self, unused_t):
        """aggregate world stocks from cell stocks"""
        self.terrestrial_carbon = sum([c.terrestrial_carbon for c in self.cells])
        self.geological_carbon = sum([c.geological_carbon for c in self.cells])


    processes = [
                 Explicit("aggregate stocks", [terrestrial_carbon, geological_carbon], aggregate_stocks),
                 Explicit("carbon preservation", [World.maritime_carbon], [
                        Nature_.total_carbon - World.atmospheric_carbon - World.terrestrial_carbon - World.geological_carbon
                    ]),
                 ODE("")
                 ]
