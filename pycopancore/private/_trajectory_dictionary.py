"""_Trajectory Dictionary Class.

This class defines the trajectory dictionary class, that is used to 
save trajectories in the runner. It inherits from dictionary and its 
aim is to have an extra save and load function, so that these processes
are easily done by the user."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


class _TrajectoryDictionary(dict):
    """Trajectory Dictionary Class.
    
    Inherits from dict"""

    def save(self,
             path):
        """Save function.
        
        Use this to save a trajectory in some format."""
        # Have a new dict to save everything to:
        dict_to_save = {}
        # Iterate through dict and replace Variables by strings of
        # Variables and Entities/taxa as strings with their uid attached.
        for key, item in self.items():
            # Go to lower level, if item is indeed another dictionary. This
            # is the case for all Variables except the time 't'!
            if isinstance(item, dict):
                new_key = str(key)
                for key_2, value in item.items():
                    # Here, key_2 are entities or taxa. Value are lists with
                    # the values the variable took during the run.

                    # First find out if key_2 is Taxon or Entity:
                    if key_2._uid:
                        # Entity:
                        new_key_2 = str(key_2) + '_' + str(key_2._uid)
                        dict_to_save[new_key][new_key_2] = value
                    else:
                        # Taxon
                        new_key_2 = str(key_2)
                        dict_to_save[new_key][new_key_2] = value
            if key == 't':
                # here we don't need to do anyhing
                dict_to_save['t'] = item
            else:
                raise Exception('neither variable nor time!')
