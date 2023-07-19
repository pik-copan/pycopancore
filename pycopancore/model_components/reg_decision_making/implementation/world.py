"""The reg decision making.world class.

"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license
import os
import pandas as pd
import numpy as np

from pycopancore.process_types import Step

from .. import interface as I


class World (I.World):
    """Define properties.
    Inherits from I.World as the interface with all necessary variables
    and parameters.
    """

    def __init__(self,
                 **kwargs
                 ):
        """Initialize an instance of World.
        """
        super(World, self).__init__(**kwargs)

    def init_individuals(self, **kwargs):
        """Initialize individuals.
        """
        cells = self.init_cells(**kwargs)
        farmers = []
        for cell in cells:
            if cell.output.cftfrac.sum("band") == 0:
                continue

            farmer = self.model.Individual(
                cell=cell,
                config=self.lpjml.config.coupled_config
            )
            farmers.append(farmer)

        farmers_sorted = sorted(farmers, key=lambda farmer: farmer.avg_hdate)
        for farmer in farmers_sorted:
            farmer.init_neighbourhood()

        return farmers_sorted, cells

    def update_individuals(self, t):
        farmers_sorted = sorted(self.individuals,
                                key=lambda farmer: farmer.avg_hdate)
        for farmer in farmers_sorted:
            farmer.update_behaviour(t)

    def update(self, t):
        self.update_individuals(t)
        self.update_output_table(t)

        self.update_lpjml(t)

    def update_output_table(self, t):
        df = self.create_output_table(t)
        self.write_output_table(df)

    def create_output_table(self, t):
        """Initialize output data"""
        # create sample time and cell data

        entities = {
            "World": "world",
            "Cell": "cell",
            "Individual": "individual",
            "SocialSystem": "social_system"
        }
        taxa = {
            "Environment": "environment",
            "Metabolism": "metabolism",
            "Culture": "culture"
        }
        core_classes = {key: value
                        for key, value in {**entities, **taxa}.items()
                        if hasattr(self.model, key) and hasattr(
                            self.lpjml.config.coupled_config.output, value
                        )}
        for copan_interface, core_class in core_classes.items():

            for var in getattr(self.lpjml.config.coupled_config.output,
                               core_class):
                df_data = {
                    'year': [t] * len(getattr(self, f"{core_class}s")),
                }

                if core_class in ["cell", "individual"]:
                    if core_class == "individual":
                        call = ".cell"
                    else:
                        call = ""

                    df_data["cell"] = [
                        eval(f"attr{call}.grid.cell.item()")
                        for attr in getattr(self, f"{core_class}s")
                    ]

                    if self.lpjml.config.coupled_config.output_settings.write_lon_lat:  # noqa
                        df_data["longitude"] = [
                            eval(f"attr{call}.grid.longitude.item()")
                            for attr in getattr(self, f"{core_class}s")
                        ]
                        df_data["latitude"] = [
                            eval(f"attr{call}.grid.latitude.item()")
                            for attr in getattr(self, f"{core_class}s")
                        ]

                    if hasattr(self.lpjml, "country"):
                        df_data["country"] = [
                            eval(f"attr{call}.country.item()")
                            for attr in getattr(self, f"{core_class}s")
                        ]
                    if hasattr(self.lpjml, "region"):
                        df_data["region"] = [
                            eval(f"attr{call}.region.item()")
                            for attr in getattr(self, f"{core_class}s")
                        ]

                variable = (
                    [eval(f"self.model.{copan_interface}.{var}.name")] * len(
                        getattr(self, f"{core_class}s")
                    )
                )

                if core_class == "world":
                    df_data["class"] = [core_class]
                    df_data["variable"] = variable
                    df_data["value"] = [
                        eval(f"self.{var}")
                    ]

                else:
                    df_data["class"] = [core_class] * len(
                        getattr(self, f"{core_class}s")
                    )
                    df_data["variable"] = variable
                    df_data["value"] = [
                        eval(f"attr.{var}")
                        for attr in getattr(self, f"{core_class}s")
                    ]

                if hasattr(eval(f"self.model.{copan_interface}.{var}.unit"), "symbol"):  # noqa
                    df_data["unit"] = [
                            eval(f"self.model.{copan_interface}.{var}.unit.symbol")  # noqa
                        ] * len(getattr(self, f"{core_class}s"))

                if "df" in locals():
                    df = pd.concat([df, pd.DataFrame(df_data)])
                else:
                    df = pd.DataFrame(df_data)

        return df

    def write_output_table(self, df):
        """Write output data"""

        mode = "w" if self.lpjml.sim_year in [
            self.lpjml.config.start_coupling, self.lpjml.config.firstyear
        ] else "a"

        # define the file name and header row
        file_name = f"{self.lpjml.config.sim_path}/output/{self.lpjml.config.sim_name}/copan_core_data.csv"  # noqa

        if not os.path.isfile(file_name) or mode == "w":
            header = True
        else:
            header = False

        df.to_csv(file_name,
                  mode=mode,
                  header=header,
                  index=False)

    processes = []
