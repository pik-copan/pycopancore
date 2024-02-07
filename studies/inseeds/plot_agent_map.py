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

# plot_dir = "/p/projects/open/Jannes/copan_core/nl_runs/plot"
plot_dir = "/p/projects/open/Jannes/copan_core/global_runs/plots"

from pycoupler.data import read_data

# output_file = "/p/projects/copan/users/lschwarz/coupling_runs/output/coupled_test"
# output_path = "/p/projects/open/Jannes/copan_core/lpjml/output/coupled_test/"
output_path = "/p/projects/open/Jannes/copan_core/global_runs/output/coupled_global_50"


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

lu_cells = all_output["cell"].unique()
# lu_cells.sort()

# Filter out NaN values from 'cell' variable
na_check = np.where(grid['cellid'].values == -999999, np.nan, grid['cellid'].values)

# Check if each value is in lu_cells
valid_cells = np.isin(na_check, lu_cells)
# valid_cells = np.logical_not(valid_cells)
all_valid_cells = valid_cells[np.newaxis, :, :]
all_valid_cells = np.repeat(all_valid_cells, len(output["time"]), axis=0)
all_valid_cells = all_valid_cells.transpose(0,2,1)

# grid['cellid'].values = grid['cellid'].values.astype(int)

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

    output[variable][:] = np.nan
    out_sub = output[variable].transpose('time', 'longitude', 'latitude')

    # replace values with those for variable of mapping
    out_sub.values[all_valid_cells] = mapping_df.values
    output[variable].values = out_sub.transpose('time', 'latitude', 'longitude').values
    output[variable].values = np.where(output[variable].values == -1e+32, np.nan, output[variable].values)


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
    
    # Increase the size of the plot
    fig, axis = plt.subplots(2, 2, figsize=(12, 7), subplot_kw=dict(projection=ccrs.PlateCarree()))
    
    # Reduce the whitespace between the plots
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, hspace=0.05, wspace=0.1) 

    fig.suptitle(f'Socio-biophysical dynamics for year {year}', fontsize=12, va="bottom", y=0.92)

    cc = rr = 0

    for variable in variables: 
        # Make lines smaller
        axis[cc, rr].add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray', linewidth=0.5)
        axis[cc, rr].add_feature(cfeature.COASTLINE, linewidth=0.5)
        
        if variable == 'agent behaviour':

            # use the colormap in the plot
            im = output[variable].loc[{'time':year}].plot(
                ax=axis[cc, rr],
                transform=ccrs.PlateCarree(),
                # xlim=[2, 10],
                # ylim=[50, 55],
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
            # Set vmin and vmax based on the variable
            if variable == "average crop yield":
                vmin, vmax = 0, 60
            elif variable == "soil organic carbon":
                vmin, vmax = 0, 6000
            else:
                vmin, vmax = np.nanmin(output[variable].values), np.nanmax(output[variable].values)

            # Clip the values to vmin and vmax
            data = np.clip(output[variable].values, vmin, vmax)

            im = output[variable].loc[{'time':year}].plot(
                ax=axis[cc, rr],
                transform=ccrs.PlateCarree(),
                # xlim=[2, 10],
                # ylim=[50, 55],
                cmap=var_cmap[variable],
                vmin=vmin,  # minimum value for the color scale
                vmax=vmax,   # maximum value for the color scale
                add_colorbar=False
            )
            # Make the colorbar smaller
            cb = plt.colorbar(im, orientation="vertical", shrink = 0.5, aspect=20)
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

imageio.mimsave(f'{plot_dir}/all_map_50.gif', var, duration=10)
