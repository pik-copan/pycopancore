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
from matplotlib import cm



#
# Plotting
#


# Building figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)
ax.view_init(13  ,210) # 13-210setting initial view. first arg:lat, second:long
#ax.set_xlim3d(-3,1)
#ax.set_ylim3d(-3,1)
ax.set_zlim3d(-0.8,2.5)

#
# Bluemarble surface_plot
#


# Create instance of Image with PIL Package
im = Image.open('./bluemarble.jpg')

# Resizing the image with scaling factor sc
# max(sc) = 1 (computational expensive)
sc = 1
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

bluemarble = ax.plot_surface(x1, y1, z1, facecolors = im, alpha = 1, antialiased = True, linewidth=1,shade=True, zorder=1)



#
# coral surface_plot as a test surface with less computational expense
#

"""
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

"""

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


# Cells1 in specified area
# Transparency and meshgrid dimension must be adjusted such that it looks nice
# TODO: different cell color due to resources (colormap) and grid
z_cells = R + 0.015
u, v = np.mgrid[1.22 * np.pi:1.31 * np.pi:20j, 0.22 * np.pi:0.29 * np.pi:20j] #first argument: longtitudonal extend, second argument latitudonal extend
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)
w = u*v
#ax.scatter(x_c,y_c,z_c, s=0.001, alpha=0.4, color='red', zorder = 2, marker='.')
#ax.plot_surface(u,v,w,rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

#u, v = np.mgrid[1.03 * np.pi:1.35 * np.pi:7j, 0.20 * np.pi:0.33 * np.pi:50j] #first argument: longtitudonal extend, second argument latitudonal extend
u, v = np.mgrid[0.68 * np.pi:1.63 * np.pi:16j, 0.1 * np.pi:0.87 * np.pi:400j]
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=0.5, alpha=1, color='black', zorder = 5, marker='|')

u, v = np.mgrid[0.68 * np.pi:1.63 * np.pi:400j, 0.1 * np.pi:0.87 * np.pi:12j] #first argument: longtitudonal extend, second argument latitudonal extend
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=0.1, alpha=1, color='black', zorder = 5, marker='|')

"""
# Cells2 in specified area

u, v = np.mgrid[1.22 * np.pi:1.31 * np.pi:20j, 0.22 * np.pi:0.29 * np.pi:20j] #first argument: longtitudonal extend, second argument latitudonal extend
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)
w = u*v
#ax.scatter(x_c,y_c,z_c, s=0.001, alpha=0.4, color='red', zorder = 2, marker='.')
#ax.plot_surface(u,v,w,rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

u, v = np.mgrid[1.06 * np.pi:1.15 * np.pi:3j, 0.22 * np.pi:0.29 * np.pi:50j] #first argument: longtitudonal extend, second argument latitudonal extend
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=0.05, alpha=1, color='black', zorder = 2, marker='_')

u, v = np.mgrid[1.06 * np.pi:1.15 * np.pi:50j, 0.22 * np.pi:0.29 * np.pi:3j] #first argument: longtitudonal extend, second argument latitudonal extend
x_c=z_cells*np.cos(u)*np.sin(v)
y_c=z_cells*np.sin(u)*np.sin(v)
z_c=z_cells*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=0.05, alpha=1, color='black', zorder = 2, marker='|')
"""

# Societies in specified area
z_soc = 2
l_soc = R + z_soc
"""
a_s = 0.06 # Shift the longtitude position to make it readable
b_s = -0.01 # ... latitude position...
u, v = np.mgrid[(1.175 + a_s) * np.pi:(1.35 + a_s)*np.pi:50j, (0.17 + b_s) * np.pi:(0.34 + b_s) * np.pi:50j]
x_c=l_soc*np.cos(u)*np.sin(v)
y_c=l_soc*np.sin(u)*np.sin(v)
z_c=l_soc*np.cos(v)

ax.scatter(x_c,y_c,z_c, s=1, alpha=0.7,depthshade=True, color='yellow', zorder=6)
"""


#other method
"""
start_lat = 1.175 * np.pi #1.21
end_lat = 1.35 * np.pi #1.35
start_lon = 0.17* np.pi # 0.17
end_lon = 0.34* np.pi # 0.34
d_lat = (end_lat - start_lat)/500



for i in range(500):
    lats_vf = start_lat + i * d_lat
    lats = np.linspace(lats_vf,lats_vf,500)
    lons = np.linspace(start_lon,end_lon,500)
    
    x_c=l_soc*np.cos(lons)*np.sin(lats)
    y_c=l_soc*np.sin(lons)*np.sin(lats)
    z_c=l_soc*np.cos(lons)
    ax.plot(x_c,y_c,z_c, linewidth=1, alpha=1, color='yellow', zorder=6)
"""


#
# Individuals 1
#



# number of individuals
N_j=9

# Individual occurances as a square on the globe
# TODO: - adjust coordinates such that it is simpler to choose them.
#       - no individual in oceans!?
lons_min = 1.25 * np.pi
lons_max = 1.4 * np.pi
lats_min = 130 * np.pi/180 # = 0.66 * pi
lats_max = 143 * np.pi/180 # = 0.83 *pi

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

###Drawing needles in two parts. First to societies, then to needle pins

# draw needles to societies
l_1 = R + z_soc # vector in r direction that points to society's location

"""
# TODO TODO TODO TODO
# get society shift from above in cartesian coordinates
s_x = (np.cos(1.175) * np.sin() - np.cos(b_s) * np.sin(a_s))
s_y = (np.sin(b_s) * np.sin(a_s) - np.sin() * np.sin())
s_z = np.cos(a_s) - np.cos()
"""

dd1 = z_soc * 150 # resolution of line
for j in range(N_j):
    x_n = np.linspace(R*x_i[j], l_1*x_i[j],dd1)
    y_n = np.linspace(R*y_i[j], l_1*y_i[j],dd1)
    z_n = np.linspace(R*z_i[j], l_1*z_i[j],dd1)
    ax.plot(x_n, y_n , z_n , color=(0.255,0,0), linewidth = 0.4, zorder = 10, linestyle = '-')

# draw needles and pin heads
z_pin = 0.02
l_2 = l_soc + z_pin # vector in r direction that points to the pin head
dd1 = z_pin * 500 # resolution of line
for j in range(N_j):
    x_n = np.linspace(l_1*x_i[j], l_2*x_i[j],dd1)
    y_n = np.linspace(l_1*y_i[j], l_2*y_i[j],dd1)
    z_n = np.linspace(l_1*z_i[j], l_2*z_i[j],dd1)
    ax.plot(x_n, y_n , z_n , color=(0.255,0,0), linewidth=0.4, zorder = 10, linestyle = "-")

# draw pin head
for i in range(N_j):
    x_n = np.linspace(l_1 * x_i[i], l_2 * x_i[i], dd1)
    y_n = np.linspace(l_1 * y_i[i], l_2 * y_i[i], dd1)
    z_n = np.linspace(l_1 * z_i[i], l_2 * z_i[i], dd1)
    p_val = np.random.rand(1)
    if p_val < 0.5:
        ax.scatter(l_2 * x_i[i], l_2 * y_i[i], l_2 * z_i[i], color = 'red', s=2, zorder = 100)
    if p_val >= 0.5:
        ax.scatter(l_2 * x_i[i], l_2 * y_i[i], l_2 * z_i[i], color = 'green', s=2, zorder = 100)
    else:
        continue

#
# Network
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
        ax.plot(l_2*xl,l_2*yl,l_2*zl, linestyle='-', color = 'blue', linewidth = 0.3, zorder=10)
    else:
        continue

#
# Individuals 2
#

# number of individuals
N_i=15

# Individual occurances as a square on the globe
# TODO: - adjust coordinates such that it is simpler to choose them.
#       - no individual in oceans!?
lons_min = 1.05 * np.pi
lons_max = 1.15 * np.pi
lats_min = 130 * np.pi/180 # = 0.66 * pi
lats_max = 140 * np.pi/180 # = 0.83 *pi

# arrays of which coordinates are randomly chosen
lons_array = np.linspace(lons_min, lons_max)
lats_array = np.linspace(lats_min, lats_max)

# create n-dim arrays for the individuals lons-lats positions
lons1_i = np.zeros(N_i)
lats1_i = np.zeros(N_i)

# coordinates to individuals
for j in range(N_i):
    lons1_i[j] = np.random.choice(lons_array)
    lats1_i[j] = np.random.choice(lats_array)

# get the cartesian coordinates from the spherical
x_i = np.cos(lons1_i) * np.sin(lats1_i)
y_i = np.sin(lons1_i) * np.sin(lats1_i)
z_i = -np.cos(lats1_i)

###Drawing needles in two parts. First to societies, then to needle pins

# draw needles to societies
l_1 = R + z_soc # vector in r direction that points to society's location

"""
# TODO TODO TODO TODO
# get society shift from above in cartesian coordinates
s_x = (np.cos(1.175) * np.sin() - np.cos(b_s) * np.sin(a_s))
s_y = (np.sin(b_s) * np.sin(a_s) - np.sin() * np.sin())
s_z = np.cos(a_s) - np.cos()
"""

dd1 = z_soc * 150 # resolution of line
for j in range(N_i):
    x_n = np.linspace(R*x_i[j], l_1*x_i[j],dd1)
    y_n = np.linspace(R*y_i[j], l_1*y_i[j],dd1)
    z_n = np.linspace(R*z_i[j], l_1*z_i[j],dd1)
    ax.plot(x_n, y_n , z_n , color=(0.255,0,0), linewidth = 0.4, zorder = 10, linestyle = '-')

# draw needles and pin heads
z_pin = 0.02
l_2 = l_soc + z_pin # vector in r direction that points to the pin head
dd1 = z_pin * 500 # resolution of line
for j in range(N_i):
    x_n = np.linspace(l_1*x_i[j], l_2*x_i[j],dd1)
    y_n = np.linspace(l_1*y_i[j], l_2*y_i[j],dd1)
    z_n = np.linspace(l_1*z_i[j], l_2*z_i[j],dd1)
    ax.plot(x_n, y_n , z_n , color=(0.255,0,0), linewidth=0.4, zorder = 10, linestyle = "-")

# draw pin head
for i in range(N_i):
    x_n = np.linspace(l_1 * x_i[i], l_2 * x_i[i], dd1)
    y_n = np.linspace(l_1 * y_i[i], l_2 * y_i[i], dd1)
    z_n = np.linspace(l_1 * z_i[i], l_2 * z_i[i], dd1)
    p_val = np.random.rand(1)
    if p_val < 0.5:
        ax.scatter(l_2 * x_i[i], l_2 * y_i[i], l_2 * z_i[i], color = 'red', s=2, zorder = 30)
    if p_val >= 0.5:
        ax.scatter(l_2 * x_i[i], l_2 * y_i[i], l_2 * z_i[i], color = 'green', s=2, zorder = 30)
    else:
        continue

#
# Network
#

#Network in own society

# Get connections in between individuals
nc = 3*N_i # number of connections

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
        l1 = np.linspace(lons1_i[p1_j],lons1_i[p2_j],50)
        l2 = np.linspace(lats1_i[p1_j],lats1_i[p2_j],50)
        #for i in range(100):
        xl = np.cos(l1) * np.sin(l2)
        yl = np.sin(l1) * np.sin(l2)
        zl = -np.cos(l2)
        ax.plot(l_2*xl,l_2*yl,l_2*zl, linestyle='-', color = 'blue', linewidth = 0.3,zorder=10)
    else:
        continue

# Network out of Society
ns = 4 # number of connections out of society

p1 = np.zeros(ns)
p2 = np.zeros(ns)

for i in range(ns):
    p1[i] = np.random.randint(0,N_i)
    p2[i] = np.random.randint(0,N_j)
    p1_i = int(p1[i])
    p2_i = int(p2[i])
    l1 = np.linspace(lons1_i[p1_i], lons_i[p2_i],100)
    l2 = np.linspace(lats1_i[p1_i], lats_i[p2_i],100)
    xl1 = np.cos(l1) * np.sin(l2)
    yl1 = np.sin(l1) * np.sin(l2)
    zl1 = -np.cos(l2)
    ax.plot(l_2 * xl1, l_2 * yl1, l_2 * zl1, linestyle='-', color=(0,0.255,0.255), linewidth=0.3, zorder=10)


plt.axis('off')
fig.savefig('example.png',dpi=1000)
#plt.show()
plt.close()
