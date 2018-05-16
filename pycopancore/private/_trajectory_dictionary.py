"""_Trajectory Dictionary Class.

This class defines the trajectory dictionary class, that is used to
save trajectories in the runner. It inherits from dictionary and its
aim is to have an extra save and load function, so that these processes
are easily done by the user."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import pickle, json, h5py
import networkx as nx
from . import _AbstractEntityMixin, _AbstractProcessTaxonMixin


class _TrajectoryDictionary(dict):
    """Trajectory Dictionary Class.

    Inherits from dict"""

    def save(self,
             *,
             filename,
             path='./',
             data_type='pickle'):
        """Save function.

        Use this to save a trajectory in some format.

        Parameters
        ----------
        filename: string
            name of the file saved
        path: string
            path or directory to save to
        data_type: string
            'pickle', 'json' or 'hdf5'
        Returns
        -------

        """
        if not data_type == "hdf5":
            # Have a new dict to save everything to:
            dict_to_save = {}
            # Iterate through dict and replace Variables by strings of
            # Variables and Entities/taxa as strings with their uid attached.
            for key, item in self.items():
                # Go to lower level, if item is indeed another dictionary. This
                # is the case for all Variables except the time 't'!
                # One could also check for isinstance(item, Variable)
                if isinstance(item, dict):
                    new_key = str(key)
                    # print('new_key',  new_key, type(new_key))
                    dict_to_save[new_key] = {}
                    for key_2, value in item.items():
                        # Here, key_2 are entities or taxa. Value are lists with
                        # the values the variable took during the run.

                        # First find out if key_2 is Taxon or Entity:
                        if isinstance(key_2, _AbstractEntityMixin):
                            # Entity:
                            new_key_2 = str(key_2)
                            # print('new_key_2', new_key_2, type(new_key_2))
                            # If values are not numbers, they have to be
                            # transformed into strings, too:
                            if all(isinstance(val, (float, int)) for val in value):
                                dict_to_save[new_key][new_key_2] = value
                            # Maybe value is a list of list with floats/ints?
                            elif (all(isinstance(val, (float, int)) for val in
                                     list(self.traverse(value)))
                                  ):
                                dict_to_save[new_key][new_key_2] = value
                            # Networks:
                            elif all(isinstance(val, nx.Graph) for val in value):
                                # save as dict of dicts
                                new_value = [nx.to_dict_of_dicts(val) for val in value]
                                # print(new_value)
                                # iterate through timesteps in list, where for every
                                # timestep there is a dictionary di in the list
                                for di in new_value:
                                    # Rewrite keys (the nodes), as they are
                                    # objects, to strings of objects:
                                    for node_key, connections in di.copy().items():
                                        di[str(node_key)] = di.pop(node_key)
                                        # Also, connections for all nodes need to
                                        # be replaced by strings:
                                        for node_key_2, connections_2 in connections.copy().items():
                                            connections[str(node_key_2)] = connections.pop(node_key_2)
                                dict_to_save[new_key][new_key_2] = new_value
                            else:
                                new_val = [str(val) for val in value]
                                dict_to_save[new_key][new_key_2] = new_val

                        elif isinstance(key_2, _AbstractProcessTaxonMixin):
                            # Taxon
                            new_key_2 = str(key_2)
                            # If values are not numbers, they have to be
                            # transformed into strings, too:
                            if all(isinstance(val, (float, int)) for val in value):
                                dict_to_save[new_key][new_key_2] = value
                            # Maybe value is a list of list with floats/ints?
                            elif (all(isinstance(val, (float, int)) for val in
                                     list(self.traverse(value)))
                                  ):
                                dict_to_save[new_key][new_key_2] = value
                            # Networks:
                            elif all(isinstance(val, nx.Graph) for val in value):
                                # save as dict of dicts
                                new_value = [nx.to_dict_of_dicts(val) for val in value]
                                # print(new_value)
                                # iterate through timesteps in list, where for every
                                # timestep there is a dictionary di in the list
                                for di in new_value:
                                    # Rewrite keys (the nodes), as they are
                                    # objects, to strings of objects:
                                    for node_key, connections in di.copy().items():
                                        di[str(node_key)] = di.pop(node_key)
                                        # Also, connections for all nodes need to
                                        # be replaced by strings:
                                        for node_key_2, connections_2 in connections.copy().items():
                                            connections[str(node_key_2)] = connections.pop(node_key_2)
                                dict_to_save[new_key][new_key_2] = new_value
                            else:
                                new_val = [str(val) for val in value]
                                dict_to_save[new_key][new_key_2] = new_val
                        else:
                            raise Exception('neither taxon nor entity')
                elif key == 't':
                    # here we don't need to do anyhing
                    dict_to_save['t'] = item
                else:
                    raise Exception('neither variable nor time!')

            # checking if all entries have the same length as time:
            # tlen = len(dict_to_save['t'])
            # for var, item in dict_to_save.items():
            #     if isinstance(item, dict):
            #         for instance, val in item.items():
            #             assert len(dict_to_save[var][instance]) == tlen, (
            #                 tlen, len(dict_to_save[var][instance]),
            #                 dict_to_save[var][instance], var, instance
            #             )

            # Add a file versio:
            dict_to_save['file-version'] = 0.1
            # Fuse Filename and path:
            # add "/" to paths if missing
            save_path = path + "/" if not path.endswith("/") else path
            # Now save as datatype:
            if data_type == 'pickle':
                save_name = save_path + filename + '.pickle'
                with open(save_name, 'wb') as dumpfile:
                    pickle.dump(dict_to_save, dumpfile, pickle.HIGHEST_PROTOCOL)
            if data_type == 'json':
                save_name = save_path + filename + '.json'
                with open(save_name, 'w') as dumpfile:
                    json.dump(dict_to_save, dumpfile)

        else:
            # HDF5 mode
            # If we want to implement this, we need to solve the following
            # problem: HDF5 and Pytables only support same datatype entries in
            # a table. If, however, an entity is deactivated during a run, all
            # its values when being idel are None (dtype:None)! Earlier values
            # might include floats, booleans, or integers. This is not possible
            # with HDF5 at all.
            raise Exception('Not implemented yet')

    # Helping function to save lists and tuples
    def traverse(self, item, tree_types=(list, tuple)):
        if isinstance(item, tree_types):
            for values in item:
                for subvalues in self.traverse(values, tree_types):
                    yield subvalues
        else:
            yield item