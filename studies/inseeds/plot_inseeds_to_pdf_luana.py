
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


output_file = "/p/projects/copan/users/lschwarz/coupling_runs/output/coupled_test_0.1/copan_core_data.csv"
# output_file = "/p/projects/open/Jannes/copan_core/deu_runs/output/coupled_test/copan_core_data.csv"
plot_path = "/p/projects/copan/users/lschwarz/core/pycopancore/studies/inseeds/pdf_plots_luana"


all_output = pd.read_csv(output_file)
ts = pd.pivot_table(all_output,
                    values='value',
                    index=['year', 'cell'],
                    columns=['variable'])

ts.query('cell == 0')
ts_mean = ts.groupby('year').mean()


# create a figure with multiple subplots
fig, axes = plt.subplots(nrows=len(ts_mean.columns), ncols=1, sharex=True, figsize=(8, 10))

# plot each variable on its own subplot
for i, col in enumerate(ts_mean.columns):
    ts_mean[col].plot(ax=axes[i], label=col)
    axes[i].set_ylabel('Mean over cells')
    axes[i].legend()

# set the x-axis label
plt.xlabel('Year')

# set the plot title
plt.suptitle('Germany: Spreading effects of (no-)till practices')

# show the plot
plt.show()

fig.savefig(f"{plot_path}/time_series_new3.pdf", bbox_inches='tight')
