#
# Use with Python 3
#

"""
TODO
----

- zorder setup
- Parameters as Individuals, cell size and coordinate choice on top
- calibration to earth coordinates
- grid of colormap to random values or so
- societies: half way up to needle pins
- transparancy issues (maybe its better to draw the  transparent colormap on
  bluemarble before doing the surface_plot)
- Matplotlib 3d has problems with the perspective. Circling the earth makes the
  picture look very weird
- implementation of ocean-water recognition due to individuals positions (maybe
  somehow with the basemap package)
- it could be possible to make a pseudo model animation (rotating earth, moving
  individuals, changing network,...)
- simplify coordinates choice for the range of individuals, society and cell
- automation of the picture perspective due to coordinate window choice such
  that it is always the best perspective
"""

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



#
# Plotting
#


# Building figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.grid(False)
ax.view_init(23,210) # 13-210setting initial view. first arg:lat, second:long
ax.set_xlim3d(-3,1)
ax.set_ylim3d(-3,1)
ax.set_zlim3d(-0.5,4.5)

#
# Bluemarble surface_plot
#

"""
# Create instance of Image with PIL Package
im = Image.open('./bluemarble.jpg')

# Resizing the image with scaling factor sc
# max(sc) = 1 (computational expensive)
sc = 5
im = im.resize([int(d/sc) for d in im.size])

# Getting np.array as RGB-Colorgrid and normalizing to python RGB-standard
im = np.array(im)/256.

# Getting arrays of coordinates for the bluemarple surface_plot.
lons1 = np.linspace(0, 360, im.shape[1]) * np.pi/180 
lats1 = np.linspace(0, 180, im.shape[0])[::-1] * np.pi/180 

# making grid for the bluemarple surface plot
R = 1 # radius of sphere
x1 = R * np.outer(np.cos(lons1), np.sin(lats1)).T
y1 = R * np.outer(np.sin(lons1), np.sin(lats1)).T
z1 = R * np.outer(np.ones(np.size(lons1)), -np.cos(lats1)).T

# drawing the bluemarble image

bluemarble = ax.plot_surface(x1, y1, z1, facecolors = im, alpha = 1, antialiased = True, linewidth=1,shade=True)
"""


#
# coral surface_plot as a test surface with less computational expense
#


# Getting arrays of coordinates for the coral surface_plot.
n1 = 360
n2 = 180
lons3 = np.linspace(0, 360, n1) * np.pi/180 
lats3 = np.linspace(0, 180, n2) * np.pi/180 

# making grid for the coral surface plot
R = 1 # radius of sphere
x1 = R * np.outer(np.cos(lons3), np.sin(lats3)).T
y1 = R * np.outer(np.sin(lons3), np.sin(lats3)).T
z1 = R * np.outer(np.ones(np.size(lons3)), -np.cos(lats3)).T

coral = ax.plot_surface(x1, y1, z1, color = "coral", alpha = 1, antialiased = True, linewidth=0.6,shade=True,rstride = 10, cstride = 10)



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
# Other sphere plots on the surface
#


# Cells in specified area
z_cells = R + 0.03
u, v = np.mgrid[1.175 * np.pi:1.35 * np.pi:200j, 0.17 * np.pi:0.34 * np.pi:200j]
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=1, alpha=0.4,depthshade=True, color='red')

# Societies in specified area
z_soc = 2
l_soc = R + z_soc
u, v = np.mgrid[1.21 * np.pi:1.35*np.pi:200j, 0.17 * np.pi:0.34 * np.pi:200j]
x_c=l_soc*np.cos(u)*np.sin(v)
y_c=l_soc*np.sin(u)*np.sin(v)
z_c=l_soc*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=1, alpha=0.4,depthshade=True, color='yellow', zorder=6)



#
# Individuals
#


# number of individuals
N_i=10 

# Individual occurances as a square on the globe
lons_min = 1.20 * np.pi
lons_max = 1.3 * np.pi
lats_min = 125 * np.pi/180 # = 0.66 * pi
lats_max = 140 * np.pi/180 # = 0.83 *pi

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

###Drawing needles in two parts. First to societies, then to needle pins

# draw needles to societies
l_1 = R + z_soc # vector in r direction that points to society location
dd1 = z_soc * 100 # resolution of line
for j in range(N_i):
    x_n = np.linspace(R*x_i[j], l_1*x_i[j],dd1)
    y_n = np.linspace(R*y_i[j], l_1*y_i[j],dd1)
    z_n = np.linspace(R*z_i[j], l_1*z_i[j],dd1)
    ax.scatter(x_n, y_n , z_n , color="black", s = 0.5, zorder = 5, depthshade = True)

# draw needles to pin heads
z_pin = 2
l_2 = l_soc + z_pin # vector in r direction that points to the pin head
dd1 = z_pin * 500 # resolution of line
for j in range(N_i):
    x_n = np.linspace(l_1*x_i[j], l_2*x_i[j],dd1)
    y_n = np.linspace(l_1*y_i[j], l_2*y_i[j],dd1)
    z_n = np.linspace(l_1*z_i[j], l_2*z_i[j],dd1)
    ax.scatter(x_n, y_n , z_n , color="black", s=0.5, zorder = 7, depthshade = True)


# draw pin head 
for i in range(N_i):
    p_val = np.random.rand(1)
    if p_val < 0.5:
        ax.scatter(l_2 * x_i[i], l_2 * y_i[i], l_2 * z_i[i], color = 'red', s=20, depthshade = True, zorder = 9)
    if p_val >= 0.5:
        ax.scatter(l_2 * x_i[i], l_2 * y_i[i], l_2 * z_i[i], color = 'green', s=20, depthshade = True, zorder = 9)
    else:
        continue

#
# Network
#

"""
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
        ax.plot(l_2*xl,l_2*yl,l_2*zl, color = 'blue', linewidth = 0.3)
    else:
        continue
"""

#plt.axis('off')
fig.savefig('example.jpg',dpi=100)
plt.show()
plt.close()
