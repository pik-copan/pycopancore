import os, glob
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import imageio
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

plot_dir = "/p/projects/open/Jannes/copan_core/nl_runs/plot"

from pycoupler.data import read_data

# output_file = "/p/projects/copan/users/lschwarz/coupling_runs/output/coupled_test"
output_path = "/p/projects/open/Jannes/copan_core/lpjml/output/coupled_test/"


all_output = pd.read_csv(f"{output_path}/copan_core_data.csv")
ts = pd.pivot_table(all_output,
                    values='value',
                    index=['year', 'cell'],
                    columns=['variable'])


# read grid information to map table values
grid = read_data(f"{output_path}/grid.nc4").astype("float32")

# read soil carbon as template for output
soilc = read_data(f"{output_path}/soilc.nc4")
output = soilc.where(soilc.time >= min(ts.index.get_level_values("year").to_list()),drop=True)

# Filter out NaN values from 'cell' variable
valid_cells = ~np.isnan(grid['cellid'].values)
all_valid_cells = valid_cells[np.newaxis, :, :]
all_valid_cells = np.repeat(all_valid_cells, len(output["time"]), axis=0)

variables = ts.columns.tolist()

for variable in variables:
    output[variable] = output['SoilC'].copy(deep=True)

    variable_df = all_output.query(f'variable == "{variable}"')

    # output = output.rename({'SoilC': variable})
    output[variable].attrs['units'] = str(variable_df.unit.unique().item())
    output[variable].attrs['long_name'] = variable_df.variable.unique().item()

    # get mapping from cell to variable
    mapping_df = variable_df.set_index(
        ['cell','year']
    )['value'].loc[grid['cellid'].values[valid_cells]]

    # transpose to get year as index
    mapping_df = mapping_df.swaplevel().sort_index()

    # replace values with those for variable of mapping
    output[variable].values[all_valid_cells] = mapping_df

# drop the 'variable_to_drop' variable from the 'dataset' dataset
output = output.drop_vars('SoilC')

# define a colormap with two colors
behaviour_cmap = ListedColormap(['purple', 'yellow'])
var_cmap = {
    'agent behaviour' : None,
    'average crop yield': 'YlGn',
    'average harvest date': 'winter',
    'soil organic carbon': 'YlOrBr'
}

for year in range(2023, 2051):
    
    fig, axis = plt.subplots(2, 2, subplot_kw=dict(projection=ccrs.PlateCarree()))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, hspace=-0.1) # set the height space between subplots
    fig.suptitle(f'Socio-biophysical dynamics for year {year}', fontsize=12, va="bottom", y=0.92)

    cc = rr = 0

    for variable in variables: 
        axis[cc, rr].add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
        axis[cc, rr].add_feature(cfeature.COASTLINE)
        
        if variable == 'agent behaviour':

            # use the colormap in the plot
            im = output[variable].loc[{'time':year}].plot(
                ax=axis[cc, rr],
                transform=ccrs.PlateCarree(),
                xlim=[2, 10],
                ylim=[50, 55],
                cmap=behaviour_cmap,
                add_colorbar=False
            )
            axis[cc, rr].legend(
                handles=[
                    mpl.patches.Patch(color='yellow', label='Conventional'),
                    mpl.patches.Patch(color='purple', label='Conservational')
                ],
                loc='lower right',
                fontsize=6
            )
            axis[cc, rr].set_title(
                f"{output[variable].attrs['long_name']}",
                fontsize=8
            )
        else:
            im = output[variable].loc[{'time':year}].plot(
                ax=axis[cc, rr],
                transform=ccrs.PlateCarree(),
                xlim=[2, 10],
                ylim=[50, 55],
                cmap=var_cmap[variable],
                vmin=np.nanmin(output[variable].values),  # minimum value for the color scale
                vmax=np.nanmax(output[variable].values),   # maximum value for the color scale
                add_colorbar=False
            )
            cb = plt.colorbar(im, orientation="vertical", shrink = 0.6)
            # cb.set_label(label=output[variable].attrs['units'], size='small')
            cb.ax.tick_params(labelsize='small')

            axis[cc, rr].set_title(
                f"{output[variable].attrs['long_name']} [{output[variable].attrs['units']}]",
                fontsize=8
            )

        if rr == 0 and cc == 0:
            rr += 1
        elif rr == 1 and cc == 0:
            cc += 1
            rr = 0
        elif rr == 0 and cc == 1:
            rr += 1

    fig.savefig(f'{plot_dir}/all_maps/raster_{year}.png', dpi=300)
    plt.close()

year_images = glob.glob(f'{plot_dir}/all_maps/raster_*')
year_images = sorted(year_images, key=lambda x: int(x.split("_")[-1].split(".")[0]))

var = [imageio.imread(file) for file in year_images]

imageio.mimsave(f'{plot_dir}/all_map.gif', var, duration=10)
