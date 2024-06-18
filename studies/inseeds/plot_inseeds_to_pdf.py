
import pandas as pd
import matplotlib.pyplot as plt

output_file = "./copan_core/global_runs/output/coupled_global_0/copan_core_data.csv"
plot_path = "./copan_core/plots"


all_output = pd.read_csv(output_file)
ts = pd.pivot_table(all_output,
                    values='value',
                    index=['year', 'cell'],
                    columns=['variable'])

ts_mean = ts.groupby('year').mean()


# create a figure with multiple subplots
fig, axes = plt.subplots(
    nrows=len(ts_mean.columns),
    ncols=1,
    sharex=True,
    figsize=(8, 10)
)

# plot each variable on its own subplot
for i, col in enumerate(ts_mean.columns):
    ts_mean[col].plot(ax=axes[i], label=col)
    axes[i].set_ylabel('Mean over cells')
    axes[i].legend()

# set the x-axis label
plt.xlabel('Year')

# set the plot title
plt.suptitle('Netherlands: Spreading effects of (no-)till practices')

# show the plot
plt.show()

fig.savefig(f"{plot_path}/time_series_nl.pdf", bbox_inches='tight')
