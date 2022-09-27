import numpy as np
import matplotlib.pyplot as plt

def plot_trajectory(list_1, list_2, t):
    for index in range(len(t)):
        plt.scatter(list_1[index], list_2[index], c="navy", )
        plt.xlabel(str(list_1))
        plt.xlabel(str(list_2))
        plt.title(f"Trajectory {str(list_1)} vs. {str(list_2)}")