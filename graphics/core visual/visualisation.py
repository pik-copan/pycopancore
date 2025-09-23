"""Visualization component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
# Use with Python 3
#
# TODO:
# - cleaning up code
# - automate a few things
# - putting important setting parameters on top

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm

#
# Plotting
#

# Building figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.grid(False)
ax.view_init(8, 213)  # 13-210setting initial view. first arg:lat, second:long
ax.set_xlim3d(-1.2, 1.2)
ax.set_ylim3d(-1.2, 1.2)
ax.set_zlim3d(-1.0, 1.0)

#
# Bluemarble surface_plot
#


# Create instance of Image with PIL Package
im = Image.open("./bluemarble4-bright-blackgrid.jpg")

# Resizing the image with scaling factor sc
# max(sc) = 1 (computational expensive)
sc = 2
im = im.resize([int(d / sc) for d in im.size])
# Getting np.array as Colorgrid and normalizing to python RGB-standard
im = np.array(im) / 256.0

# Getting arrays of coordinates for the bluemarple surface_plot.
lons = np.linspace(0, 360, im.shape[1]) * np.pi / 180
lats = np.linspace(0, 180, im.shape[0]) * np.pi / 180

# making grid for the bluemarple surface plot
R = 1  # radius of sphere
x = R * np.outer(np.cos(lons), np.sin(lats)).T
y = R * np.outer(np.sin(lons), np.sin(lats)).T
z = R * np.outer(np.ones(np.size(lons)), np.cos(lats)).T

# drawing the bluemarble image

bluemarble = ax.plot_surface(
    x,
    y,
    z,
    facecolors=im,
    alpha=1,
    linewidth=0,
    rstride=1,
    cstride=2,
    shade=False,
    zorder=1,
)

"""
#
# Meshgrid
#

lons1 = 125 * np.pi/180
lons2 =  305 * np.pi/180
lats1 = 0
lats2 = np.pi
lons_i = np.linspace(lons1,lons2,17)
lats_i =  np.linspace(lats1,lats2, 100)
for i in range(17):
    x_i = (R) * np.cos(lons_i[i]) * np.sin(lats_i)
    y_i = (R) * np.sin(lons_i[i]) * np.sin(lats_i)
    z_i = -(R) * np.cos(lats_i)
    ax.plot(x_i,y_i,z_i, color = 'black', linewidth = 1, linestyle = '-')


lons_i = np.linspace(lons1, lons2, 100)
lats_i = np.linspace(lats1, lats2, 17)

for i in range(17):
    x_i = (R) * np.cos(lons_i) * np.sin(lats_i[i])
    y_i = (R) * np.sin(lons_i) * np.sin(lats_i[i])
    z_i = -(R) * np.cos(lats_i[i])
    ax.plot(x_i,y_i,z_i, color = 'black', linewidth = 1, linestyle = '-')
"""

#
# Societes and Cells group 1
#
r_soc = 1 + 0.5

# Since this social_system has a different shape it is done in two steps

# step 1: first part of social_system
start_lat = 0.7345 * np.pi  # 1.21
end_lat = 0.796 * np.pi  # 1.35
start_lon = 1.34 * np.pi  # 1.33 for sc=4 and grid=5: 1 pixel is 0.005
end_lon = 1.47 * np.pi  # 1.48
d_lat = (end_lat - start_lat) / 500

for i in range(500):
    lats_vf = start_lat + i * d_lat
    lats = np.linspace(lats_vf, lats_vf, 500)
    lons = np.linspace(start_lon, end_lon, 500)

    x_c = r_soc * np.cos(lons) * np.sin(lats)
    y_c = r_soc * np.sin(lons) * np.sin(lats)
    z_c = -r_soc * np.cos(lats)
    ax.plot(x_c, y_c, z_c, linewidth=1, alpha=0.1, color="yellow", zorder=6)

#
# step 2: second part of social_system
#

start_lat = 0.667 * np.pi  # 1.21
end_lat = 0.7345 * np.pi  # 1.35
start_lon = 1.405 * np.pi  # 1.33 for sc=4 and grid=5: 1 pixel is 0.005
end_lon = 1.47 * np.pi  # 1.48
d_lat = (end_lat - start_lat) / 500

for i in range(500):
    lats_vf = start_lat + i * d_lat
    lats = np.linspace(lats_vf, lats_vf, 500)
    lons = np.linspace(start_lon, end_lon, 500)

    x_c = r_soc * np.cos(lons) * np.sin(lats)
    y_c = r_soc * np.sin(lons) * np.sin(lats)
    z_c = -r_soc * np.cos(lats)
    ax.plot(x_c, y_c, z_c, linewidth=1, alpha=0.1, color="yellow", zorder=6)

#
# Individuals group 1
#


# number of individuals
N_i = 14

# Individual occur as two squares on the globe
# first square
lons_min1 = 1.41 * np.pi
lons_max1 = 1.46 * np.pi
lats_min1 = 0.669 * np.pi  # = 0.66 * pi
lats_max1 = 0.73 * np.pi  # = 0.83 *pi

# second square
lons_min2 = 1.35 * np.pi
lons_max2 = 1.46 * np.pi
lats_min2 = 0.74 * np.pi  # = 0.66 * pi
lats_max2 = 0.79 * np.pi  # = 0.83 *pi


# arrays of which coordinates are randomly chosen
lons_array1 = np.linspace(lons_min1, lons_max1)
lats_array1 = np.linspace(lats_min1, lats_max1)

lons_array2 = np.linspace(lons_min2, lons_max2)
lats_array2 = np.linspace(lats_min2, lats_max2)

lons_array = np.zeros((lons_array1.size + lons_array2.size))
lats_array = np.zeros((lats_array1.size + lats_array2.size))

lons_array[0 : lons_array1.size : 1] = lons_array1
lons_array[lons_array1.size : (lons_array1.size + lons_array2.size) : 1] = (
    lons_array2  # noqa: E501
)

lats_array[0 : lats_array1.size : 1] = lats_array1
lats_array[lats_array1.size : (lats_array1.size + lats_array2.size) : 1] = (
    lats_array2  # noqa: E501
)

# create n-dim arrays for the individuals lons-lats positions
lons1_i = np.zeros(N_i)
lats1_i = np.zeros(N_i)

# coordinates to individuals
j = 0
while j < N_i:
    lons1_i[j] = np.random.choice(lons_array)
    if lons1_i[j] in lons_array1:
        lats1_i[j] = np.random.choice(lats_array1)
    if lons1_i[j] in lons_array2:
        lats1_i[j] = np.random.choice(lats_array2)
    j += 1

# get the cartesian coordinates from the spherical
x_i = np.cos(lons1_i) * np.sin(lats1_i)
y_i = np.sin(lons1_i) * np.sin(lats1_i)
z_i = -np.cos(lats1_i)

# draw needles and pin heads

z_pin = 2.3
dd1 = z_pin * 500  # resolution of line
# The following for-loop includes two identical 'ax.scatter' functions. This is
# necessary since a buzg occured without them (The first drawn pin-head was not
# in the foreground)
for j in range(N_i):
    p_val = np.random.rand(1)
    if p_val < 0.5:
        x_n = np.linspace(R * x_i[j], (R + 0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R + 0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R + 0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R + 0.5) * x_i[j], (z_pin - 0.019) * x_i[j], dd1)
        y_n = np.linspace((R + 0.5) * y_i[j], (z_pin - 0.019) * y_i[j], dd1)
        z_n = np.linspace((R + 0.5) * z_i[j], (z_pin - 0.019) * z_i[j], dd1)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="red",
            s=10,
            zorder=10,  # noqa: E501
        )
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=7)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="red",
            s=10,
            zorder=10,  # noqa: E501
        )
    if p_val >= 0.5:
        x_n = np.linspace(R * x_i[j], (R + 0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R + 0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R + 0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R + 0.5) * x_i[j], (z_pin - 0.019) * x_i[j], dd1)
        y_n = np.linspace((R + 0.5) * y_i[j], (z_pin - 0.019) * y_i[j], dd1)
        z_n = np.linspace((R + 0.5) * z_i[j], (z_pin - 0.019) * z_i[j], dd1)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="green",
            s=10,
            zorder=10,
        )
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=7)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="green",
            s=10,
            zorder=10,
        )
    else:
        continue

#
# Network Group 1
#


# Get connections in between individuals
nc = 2 * N_i  # number of connections

# arrays for connections to avoid double connections (not necessary in current
# code)
p1 = np.zeros(nc)
p2 = np.zeros(nc)

# xl = []
# yl = []
# zl = []

for j in range(nc):
    p1[j] = np.random.randint(0, N_i)
    p2[j] = np.random.randint(0, N_i)
    p1_j = int(p1[j])  # to solve an int-value error in the loop
    p2_j = int(p2[j])
    if p1[j] != p2[j]:
        l1 = np.linspace(lons1_i[p1_j], lons1_i[p2_j], 50)
        l2 = np.linspace(lats1_i[p1_j], lats1_i[p2_j], 50)
        for i in range(100):
            xl = np.cos(l1) * np.sin(l2)
            yl = np.sin(l1) * np.sin(l2)
            zl = -np.cos(l2)
        ax.plot(
            z_pin * xl,
            z_pin * yl,
            z_pin * zl,
            linestyle="-",
            color="blue",
            linewidth=0.3,
        )
    else:
        continue


#
# Group 2
#

#
# Societes and Cells group 2
#

r_soc = 1 + 0.5

start_lat = 0.7345 * np.pi  # 1.21
end_lat = 0.796 * np.pi  # 1.35
start_lon = 1.008 * np.pi  # 0.17
end_lon = 1.134 * np.pi  # 0.34
d_lat = (end_lat - start_lat) / 500

for i in range(500):
    lats_vf = start_lat + i * d_lat
    lats = np.linspace(lats_vf, lats_vf, 500)
    lons = np.linspace(start_lon, end_lon, 500)

    x_c = r_soc * np.cos(lons) * np.sin(lats)
    y_c = r_soc * np.sin(lons) * np.sin(lats)
    z_c = -r_soc * np.cos(lats)
    ax.plot(x_c, y_c, z_c, linewidth=1, alpha=0.1, color="yellow", zorder=6)

#
# Individuals group 2
#

z_soc = 2.3
l_soc = R + z_soc

# number of individuals
N_j = 9

# Individual occur in a square on the globe
lons_min = 1.01 * np.pi
lons_max = 1.13 * np.pi
lats_min = 0.736 * np.pi  # = 0.66 * pi
lats_max = 0.79 * np.pi  # = 0.83 *pi

# arrays of which coordinates are randomly chosen
lons_array = np.linspace(lons_min, lons_max)
lats_array = np.linspace(lats_min, lats_max)

# create n-dim arrays for the individuals lons-lats positions
lons2_i = np.zeros(N_j)
lats2_i = np.zeros(N_j)

# coordinates to individuals
for j in range(N_j):
    lons2_i[j] = np.random.choice(lons_array)
    lats2_i[j] = np.random.choice(lats_array)

# get the cartesian coordinates from the spherical
x_i = np.cos(lons2_i) * np.sin(lats2_i)
y_i = np.sin(lons2_i) * np.sin(lats2_i)
z_i = -np.cos(lats2_i)

# draw needles and pin heads

z_pin = 2.3
dd1 = z_pin * 500  # resolution of line
# The following for-loop includes two identical 'ax.scatter' functions. This is
# necessary since a buzg occured without them (The first drawn pin-head was not
# in the foreground)
for j in range(N_j):
    p_val = np.random.rand(1)
    if p_val < 0.5:
        x_n = np.linspace(R * x_i[j], (R + 0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R + 0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R + 0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R + 0.5) * x_i[j], (z_pin - 0.019) * x_i[j], dd1)
        y_n = np.linspace((R + 0.5) * y_i[j], (z_pin - 0.019) * y_i[j], dd1)
        z_n = np.linspace((R + 0.5) * z_i[j], (z_pin - 0.019) * z_i[j], dd1)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="red",
            s=10,
            zorder=10,  # noqa: E501
        )
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=7)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="red",
            s=10,
            zorder=10,  # noqa: E501
        )
    if p_val >= 0.5:
        x_n = np.linspace(R * x_i[j], (R + 0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R + 0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R + 0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R + 0.5) * x_i[j], (z_pin - 0.019) * x_i[j], dd1)
        y_n = np.linspace((R + 0.5) * y_i[j], (z_pin - 0.019) * y_i[j], dd1)
        z_n = np.linspace((R + 0.5) * z_i[j], (z_pin - 0.019) * z_i[j], dd1)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="green",
            s=10,
            zorder=10,
        )
        ax.plot(x_n, y_n, z_n, "black", linewidth=0.4, linestyle="-", zorder=7)
        ax.scatter(
            z_pin * x_i[j],
            z_pin * y_i[j],
            z_pin * z_i[j],
            color="green",
            s=10,
            zorder=10,
        )
    else:
        continue


#
# Network Group 2
#


# Get connections in between individuals
nc = 2 * N_j  # number of connections

# arrays for connections to avoid double connections (not necessary in current
# code)
p1 = np.zeros(nc)
p2 = np.zeros(nc)

# xl = []
# yl = []
# zl = []

for j in range(nc):
    p1[j] = np.random.randint(0, N_j)
    p2[j] = np.random.randint(0, N_j)
    p1_j = int(p1[j])  # to solve an int-value error in the loop
    p2_j = int(p2[j])
    if p1[j] != p2[j]:
        l1 = np.linspace(lons2_i[p1_j], lons2_i[p2_j], 50)
        l2 = np.linspace(lats2_i[p1_j], lats2_i[p2_j], 50)
        for i in range(100):
            xl = np.cos(l1) * np.sin(l2)
            yl = np.sin(l1) * np.sin(l2)
            zl = -np.cos(l2)
        ax.plot(
            z_pin * xl,
            z_pin * yl,
            z_pin * zl,
            linestyle="-",
            color="blue",
            linewidth=0.3,
        )
    else:
        continue


#
# Network out of social_systems
#

ns = 7  # number of connections out of social_system

p1 = np.zeros(ns)
p2 = np.zeros(ns)

for i in range(ns):
    p1[i] = np.random.randint(0, N_i)
    p2[i] = np.random.randint(0, N_j)
    p1_i = int(p1[i])
    p2_i = int(p2[i])
    l1 = np.linspace(lons1_i[p1_i], lons2_i[p2_i], 100)
    l2 = np.linspace(lats1_i[p1_i], lats2_i[p2_i], 100)
    xl1 = np.cos(l1) * np.sin(l2)
    yl1 = np.sin(l1) * np.sin(l2)
    zl1 = -np.cos(l2)
    ax.plot(
        z_pin * xl1,
        z_pin * yl1,
        z_pin * zl1,
        linestyle="-",
        color="blue",
        linewidth=0.3,
        zorder=10,
    )


plt.axis("off")
fig.savefig("example.jpg", bbox_inches="tight", dpi=400)
# plt.show()
plt.close()
