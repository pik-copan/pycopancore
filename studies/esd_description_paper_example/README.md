# Introduction
Due to some issues with setting the seed for generating random numbers in the
current implementation of `pycopancore` the following scripts *qualitatively*
reproduce the results show in Figure 5 and Figure 6 of the description paper
currently available at https://arxiv.org/abs/1909.13697

# Plot figure 5
Run the following code:
```
python run_esd_example.py -p 0.25 -s 0
python run_esd_example.py -p 0.4 -s 0 -u 12 --with-social
python plot_figure5.py
```