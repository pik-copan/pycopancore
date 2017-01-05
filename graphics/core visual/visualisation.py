#
# Use with Python 3
#

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm



#
# Plotting
#


# Building figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)
ax.view_init(8  ,215) # 13-210setting initial view. first arg:lat, second:long
ax.set_xlim3d(-1.2,1.2)
ax.set_ylim3d(-1.2,1.2)
ax.set_zlim3d(-1,1)

#
# Bluemarble surface_plot
#


# Create instance of Image with PIL Package
im = Image.open('./bluemarble.jpg')

# Resizing the image with scaling factor sc
# max(sc) = 1 (computational expensive)
sc = 1
im = im.resize([int(d/sc) for d in im.size])

# Getting np.array as Colorgrid and normalizing to python RGB-standard
im = np.array(im)/256.

# Getting arrays of coordinates for the bluemarple surface_plot.
lons = np.linspace(0, 360, im.shape[1]) * np.pi/180
lats = np.linspace(0, 180, im.shape[0]) * np.pi/180

# making grid for the bluemarple surface plot
R = 1 # radius of sphere
x = R * np.outer(np.cos(lons), np.sin(lats)).T
y = R * np.outer(np.sin(lons), np.sin(lats)).T
z = R * np.outer(np.ones(np.size(lons)), np.cos(lats)).T

# drawing the bluemarble image

bluemarble = ax.plot_surface(x, y, z, facecolors = im, alpha = 1, antialiased = True, linewidth=1,shade=True, zorder=1)


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

#
# Societes and Cells group 1
#

start_lat = 0.69 * np.pi  # 1.21
end_lat = 0.815 * np.pi  # 1.35
start_lon = 1.325 * np.pi  # 0.17
end_lon = 1.5 * np.pi  # 0.34
d_lat = (end_lat - start_lat) / 500

for i in range(500):
    lats_vf = start_lat + i * d_lat
    lats = np.linspace(lats_vf, lats_vf, 500)
    lons = np.linspace(start_lon, end_lon, 500)

    x_c = (R+0.5) * np.cos(lons) * np.sin(lats)
    y_c = (R+0.5) * np.sin(lons) * np.sin(lats)
    z_c = -(R+0.5) * np.cos(lats)
    ax.plot(x_c, y_c, z_c, linewidth=1, alpha=0.2, color='yellow', zorder=6)

#
# Individuals group 1
#

z_soc = 2.3
l_soc = R + z_soc

# number of individuals
N_j=15

# Individual occur as a square on the globe
lons_min = 1.33 * np.pi
lons_max = 1.47 * np.pi
lats_min = 0.70 * np.pi # = 0.66 * pi
lats_max = 0.79 * np.pi # = 0.83 *pi

# arrays of which coordinates are randomly chosen
lons_array = np.linspace(lons_min, lons_max)
lats_array = np.linspace(lats_min, lats_max)

# create n-dim arrays for the individuals lons-lats positions
lons_i = np.zeros(N_j)
lats_i = np.zeros(N_j)

# coordinates to individuals
for j in range(N_j):
    lons_i[j] = np.random.choice(lons_array)
    lats_i[j] = np.random.choice(lats_array)

# get the cartesian coordinates from the spherical
x_i = np.cos(lons_i) * np.sin(lats_i)
y_i = np.sin(lons_i) * np.sin(lats_i)
z_i = -np.cos(lats_i)

# draw needles and pin heads

z_pin = 2.3
dd1 = z_pin * 500 # resolution of line
# The following for-loop includes two identical 'ax.scatter' functions. This is
# necessary since a buzg occured without them (The first drawn pin-head was not
# in the foreground)
for j in range(N_j):
    p_val = np.random.rand(1)
    if p_val < 0.5:
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j], color='red',
                   s=2, zorder=10)
        x_n = np.linspace(R * x_i[j], (R+0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R+0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R+0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R+0.5) * x_i[j], z_pin * x_i[j], dd1)
        y_n = np.linspace((R+0.5) * y_i[j], z_pin * y_i[j], dd1)
        z_n = np.linspace((R+0.5) * z_i[j], z_pin * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=10)
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j], color='red',
                   s=2, zorder=100)
    if p_val >= 0.5:
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j],
                   color='green', s=2, zorder=10)
        x_n = np.linspace(R * x_i[j], (R+0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R+0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R+0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R + 0.5) * x_i[j], z_pin * x_i[j], dd1)
        y_n = np.linspace((R + 0.5) * y_i[j], z_pin * y_i[j], dd1)
        z_n = np.linspace((R + 0.5) * z_i[j], z_pin * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=10)
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j],
                   color='green', s=2, zorder=100)
    else:
        continue

#
# Network Group 1
#


# Get connections in between individuals
nc = 3 * N_j  # number of connections

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
        l1 = np.linspace(lons_i[p1_j], lons_i[p2_j], 50)
        l2 = np.linspace(lats_i[p1_j], lats_i[p2_j], 50)
        for i in range(100):
            xl = np.cos(l1) * np.sin(l2)
            yl = np.sin(l1) * np.sin(l2)
            zl = -np.cos(l2)
        ax.plot(z_pin * xl, z_pin * yl, z_pin * zl, linestyle='-', color='blue',
                    linewidth=0.3)
    else:
        continue


#
###
### Group 2
### -------
###
#


#
# Societes and Cells group 2
#

start_lat = 0.7525 * np.pi  # 1.21
end_lat = 0.815 * np.pi  # 1.35
start_lon = 1.01 * np.pi  # 0.17
end_lon = 1.13 * np.pi  # 0.34
d_lat = (end_lat - start_lat) / 500

for i in range(500):
    lats_vf = start_lat + i * d_lat
    lats = np.linspace(lats_vf, lats_vf, 500)
    lons = np.linspace(start_lon, end_lon, 500)

    x_c = (R+0.5) * np.cos(lons) * np.sin(lats)
    y_c = (R+0.5) * np.sin(lons) * np.sin(lats)
    z_c = -(R+0.5) * np.cos(lats)
    ax.plot(x_c, y_c, z_c, linewidth=1, alpha=0.15, color='yellow', zorder=6)

#
# Individuals group 2
#

z_soc = 2.3
l_soc = R + z_soc

# number of individuals
N_j=6

# Individual occur in a square on the globe
lons_min = 1.03 * np.pi
lons_max = 1.12 * np.pi
lats_min = 0.76 * np.pi # = 0.66 * pi
lats_max = 0.79 * np.pi # = 0.83 *pi

# arrays of which coordinates are randomly chosen
lons_array = np.linspace(lons_min, lons_max)
lats_array = np.linspace(lats_min, lats_max)

# create n-dim arrays for the individuals lons-lats positions
lons_i = np.zeros(N_j)
lats_i = np.zeros(N_j)

# coordinates to individuals
for j in range(N_j):
    lons_i[j] = np.random.choice(lons_array)
    lats_i[j] = np.random.choice(lats_array)

# get the cartesian coordinates from the spherical
x_i = np.cos(lons_i) * np.sin(lats_i)
y_i = np.sin(lons_i) * np.sin(lats_i)
z_i = -np.cos(lats_i)

# draw needles and pin heads

z_pin = 2.3
dd1 = z_pin * 500 # resolution of line
# The following for-loop includes two identical 'ax.scatter' functions. This is
# necessary since a buzg occured without them (The first drawn pin-head was not
# in the foreground)
for j in range(N_j):
    p_val = np.random.rand(1)
    if p_val < 0.5:
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j], color='red',
                   s=2, zorder=10)
        x_n = np.linspace(R * x_i[j], (R+0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R+0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R+0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R+0.5) * x_i[j], z_pin * x_i[j], dd1)
        y_n = np.linspace((R+0.5) * y_i[j], z_pin * y_i[j], dd1)
        z_n = np.linspace((R+0.5) * z_i[j], z_pin * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=10)
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j], color='red',
                   s=2, zorder=10)
    if p_val >= 0.5:
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j],
                   color='green', s=2, zorder=10)
        x_n = np.linspace(R * x_i[j], (R+0.5) * x_i[j], dd1)
        y_n = np.linspace(R * y_i[j], (R+0.5) * y_i[j], dd1)
        z_n = np.linspace(R * z_i[j], (R+0.5) * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=1)
        x_n = np.linspace((R + 0.5) * x_i[j], z_pin * x_i[j], dd1)
        y_n = np.linspace((R + 0.5) * y_i[j], z_pin * y_i[j], dd1)
        z_n = np.linspace((R + 0.5) * z_i[j], z_pin * z_i[j], dd1)
        ax.plot(x_n, y_n, z_n, 'black', linewidth=0.4, linestyle="-", zorder=10)
        ax.scatter(z_pin * x_i[j], z_pin * y_i[j], z_pin * z_i[j],
                   color='green', s=2, zorder=10)
    else:
        continue


#
# Network Group 2
#


# Get connections in between individuals
nc = 3*N_j # number of connections

# arrays for connections to avoid double connections (not necessary in current
# code)
p1 = np.zeros(nc)
p2 = np.zeros(nc)

#xl = []
#yl = []
#zl = []

for j in range(nc):
    p1[j] = np.random.randint(0,N_j)
    p2[j] = np.random.randint(0,N_j)
    p1_j = int(p1[j]) # to solve an int-value error in the loop
    p2_j = int(p2[j])
    if p1[j] !=  p2[j]:
        l1 = np.linspace(lons_i[p1_j],lons_i[p2_j],50)
        l2 = np.linspace(lats_i[p1_j],lats_i[p2_j],50)
        for i in range(100):
            xl = np.cos(l1) * np.sin(l2)
            yl = np.sin(l1) * np.sin(l2)
            zl = -np.cos(l2)
        ax.plot(z_pin * xl, z_pin * yl, z_pin * zl, linestyle='-', color='blue',
                    linewidth=0.3)
    else:
        continue

plt.axis('off')
fig.savefig('example.png',dpi=1000)
#plt.show()
plt.close()
