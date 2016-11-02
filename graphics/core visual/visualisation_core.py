#
# Use with Python 3
#

"""
TODO
----

- calibration to earth coordinates
- grid of colormap to random values or so
- societies: half way up to needle pins
- transparancy issues (maybe its better to draw the  transparent colormap on
bluemarble before doing the surface_plot)
- implementation of ocean-water recognition due to individuals positions (maybe
somehow with the basemap package)
- it could be possible to make a pseudo model animation (rotating earth, moving individuals, changing network,...)
"""

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


#
# Export and scaling of Image
#


# Create instance of Image with PIL Package
im = Image.open('./bluemarble.jpg')

# Resizing the image with scaling factor sc
# max(sc) = 1 (computational expensive)
sc = 10
im = im.resize([int(d/sc) for d in im.size])

# Getting np.array as RGB-Colorgrid and normalizing to python RGB-standard
im = np.array(im)/256.



#
# Plotting Process
#


# Building figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.grid(False)
ax.view_init(13,210) # 13-210setting initial view. first arg:lat, second:long
ax.set_xlim3d(-2.5,1)
ax.set_ylim3d(-2.5,1)
ax.set_zlim3d(-0.5,2.5)

#
# Bluemarble surface_plot
#


# Getting arrays of coordinates for the bluemarple surface_plot.
lons1 = np.linspace(0, 360, im.shape[1]) * np.pi/180 
lats1 = np.linspace(0, 180, im.shape[0])[::-1] * np.pi/180 

# making grid for the bluemarple surface plot
R = 1 # radius of sphere
x1 = R * np.outer(np.cos(lons1), np.sin(lats1)).T
y1 = R * np.outer(np.sin(lons1), np.sin(lats1)).T
z1 = R * np.outer(np.ones(np.size(lons1)), -np.cos(lats1)).T

# drawing the bluemarble image
bluemarble = ax.plot_surface(x1, y1, z1, facecolors = im, alpha = 1, antialiased = True, linewidth=0,shade=False)


#
# Colormap surface_plot (to symbolize the cell stocks)
#

"""
# Getting lons, lats arrays with resolution n1,n2
n1 = 360
n2 = 180
lons2 = np.linspace(0, 360, n1) * np.pi/180 
lats2 = np.linspace(0, 180, n2) * np.pi/180 

# making grid of the colormap
# The radius should be slightly larger then of bluemarble
x2 = (R+0.01) * np.outer(np.cos(lons2), np.sin(lats2)).T
y2 = (R+0.01) * np.outer(np.sin(lons2), np.sin(lats2)).T
z2 = (R+0.01) * np.outer(np.ones(np.size(lons2)), -np.cos(lats2)).T

# drawing a transparent colormap onto the bluemarble image
colormap = ax.plot_surface(x2, y2, z2, cmap = "hot", rstride=10,cstride=10, alpha = 0.3, antialiased = True, linewidth = 0.5, shade=False)
# colorbar that shows stock value
    #fig.colorbar(colormap)
"""

#
# Other surface sphere plots methods
#


"""
z = R + 0.01 
u, v = np.mgrid[0:2*np.pi:2000j, 0:np.pi:1000j]
x_c=z*np.cos(u)*np.sin(v)
y_c=z*np.sin(u)*np.sin(v)
z_c=z*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=1, alpha=0.3,depthshade=False, color='red')
"""


#
# Individuals
#


# number of individuals
N_i=20 

# Individual occurances as a square on the globe
lons_min = 220 * np.pi/180
lons_max = 270 * np.pi/180
lats_min = 120 * np.pi/180
lats_max = 150 * np.pi/180

# arrays of which coordinates are randomly chosen
lons_array = np.linspace(lons_min, lons_max)
lats_array = np.linspace(lats_min, lats_max)

# create n-dim arrays for the individuals lons-lats positions
lons_i = np.zeros(N_i)
lats_i = np.zeros(N_i)

# coordinates to individuals
for j in range(N_i):
    lons_i[j] = np.random.choice(lons_array)
    lats_i[j] = np.random.choice(lats_array)

# get the cartesian coordinates from the spherical
x_i = np.cos(lons_i) * np.sin(lats_i)
y_i = np.sin(lons_i) * np.sin(lats_i)
z_i = -np.cos(lats_i)

# draw needles of length r
r = 2
l = R + r # vector in r direction that points to the pin head
dd1 = r * 100 # resolution of line
for j in range(N_i):
    x_n = np.linspace(R*x_i[j], l*x_i[j],dd1)
    y_n = np.linspace(R*y_i[j], l*y_i[j],dd1)
    z_n = np.linspace(R*z_i[j], l*z_i[j],dd1)
    ax.plot(x_n, y_n , z_n , color="black", linewidth = 0.5)

# draw pin head 
for i in range(N_i):
    p_val = np.random.rand(1)
    if p_val < 0.5:
        ax.scatter(l * x_i[i], l * y_i[i], l * z_i[i], color = 'red', s=25)
    if p_val >= 0.5:
        ax.scatter(l * x_i[i], l * y_i[i], l * z_i[i], color = 'green', s=25)
    else:
        continue

#
# Network
#


# Get connections in between individuals
nc = 5*N_i # number of connections

# arrays for connections to avoid double connections (not necessary in current
# code)
p1 = np.zeros(nc)
p2 = np.zeros(nc) 

#xl = []
#yl = []
#zl = []

for j in range(nc):
    p1[j] = np.random.randint(0,N_i)
    p2[j] = np.random.randint(0,N_i)
    p1_j = int(p1[j]) # to solve an int-value error in the loop
    p2_j = int(p2[j])
    if p1[j] !=  p2[j]:
        l1 = np.linspace(lons_i[p1_j],lons_i[p2_j],100)
        l2 = np.linspace(lats_i[p1_j],lats_i[p2_j],100)
        for i in range(100):
            xl = np.cos(l1) * np.sin(l2)
            yl = np.sin(l1) * np.sin(l2)
            zl = -np.cos(l2)
        ax.plot(l*xl,l*yl,l*zl, color = 'blue', linewidth = 0.3)
    else:
        continue

#plt.axis('off')
fig.savefig('example.png',dpi=1000)
plt.show()
