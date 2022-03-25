import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay
from matplotlib.patches import Polygon
from math import sqrt
from sys import argv


visualisationMode = 1

# nloop = int(argv[1])
# nc = int(argv[2])

# # Read cell positions from file
# data = np.genfromtxt(argv[3]+"/cellpositions.txt")
# conditions = np.genfromtxt(argv[3]+"/initialconditions.txt")

# #nc = int(conditions[0,1]*3.0)
# PMZwidth = conditions[7,1]
# PMZheight = conditions[8,1]
# CEwidth = conditions[9,1]
# CMwidth = conditions[10,1]
# Clength = conditions[11,1]
# chainShape = conditions[15,1]

# nc = int(argv[1])
# nloop = int(argv[2])
# PMZwidth = float(argv[3])
# PMZheight = float(argv[4])
# CEwidth = float(argv[5])
# CMwidth = float(argv[6])
# Clength = float(argv[7])
# chainShape = conditions[12,1]

# Read cell positions from file
filepath = argv[10]
data = np.genfromtxt(filepath +"/cellpositions.txt")
nc = int(argv[1])
nloop = int(argv[2])
PMZwidth = float(argv[3])
PMZheight = float(argv[4])
CEwidth = float(argv[5])
CMwidth = float(argv[6])
Clength = float(argv[7])
chainShape = int(argv[8])
mz_to_pmz_height_ratio = float(argv[9])
alpha = 1


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Function from https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647#20678647
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")
    new_regions = []
    new_vertices = vor.vertices.tolist()
    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()
    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))
    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]
        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue
        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]
        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue
            # Compute the missing endpoint of an infinite ridge
            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())
        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]
        # finish
        new_regions.append(new_region.tolist())
    return new_regions, np.asarray(new_vertices)


# Important bit starts here
# (137, 43, 107, 255)
#color_list = ["lightskyblue","mediumspringgreen","magenta"]
color_list = [(0.8313725490196079, 0.8313725490196079, 0.8313725490196079, 1.0),
            (0.23529411764705882, 0.7333333333333333, 0.7294117647058823, 1.0),
            (0.5372549019607843, 0.16862745098039217, 0.4196078431372549, 1.0)]
xmax=1.5   # Size of plots
fig,ax=plt.subplots()

plt.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
plt.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)
ax.axis('equal')

# notochord = matplotlib.patches.Rectangle((-2*PMZwidth, -PMZheight/2 -Clength -PMZheight*2),
#                 width = 4*PMZwidth,
#                 height= PMZheight,
#                 alpha= 0.3,
#                 fc = 'orchid')
# ax.add_patch(notochord)

# notochord_label = ax.text(-1.5*PMZwidth,
#               -PMZheight/2.0 - Clength -PMZheight -PMZheight/2,
#               '',
#               ha='center',
#               va='center',
#               fontsize=12,
#               color = 'k',
#               fontweight='bold')
# notochord_label.set_text('notochord')


if chainShape == 1:
    diamondOffset = (CMwidth-CEwidth)/2.0
    ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,CEwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,CEwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0],[diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0],[diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)

if chainShape == 2:
    # Top strip
    ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=alpha,linewidth=0)
    # Left strip
    ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    # Right strip
    ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    # # Bottom strip
    # #ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=alpha,linewidth=0)

    # Add four grey squares around MiddleZone

    left_top = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength),
    width = (PMZwidth - CEwidth)/2,
    height= Clength,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(left_top)

    right_top = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength),
    width = (PMZwidth - CEwidth)/2,
    height= Clength,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(right_top)

    left_bottom = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength - PMZheight*4),
    width = (PMZwidth - CEwidth)/2,
    height= PMZheight*3,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(left_bottom)

    right_bottom = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength - PMZheight*4),
    width = (PMZwidth - CEwidth)/2,
    height= PMZheight*3,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(right_bottom)

if chainShape == 3:
    # Top strip
    ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=alpha,linewidth=0)
    # Left strip
    ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    # Right strip
    ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    # # Bottom strip
    # #ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=alpha,linewidth=0)

    # Add four grey squares around MiddleZone

    left_top = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength),
    width = (PMZwidth - CEwidth)/2,
    height= Clength,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(left_top)

    right_top = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength),
    width = (PMZwidth - CEwidth)/2,
    height= Clength,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(right_top)

    left_bottom = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength - PMZheight*mz_to_pmz_height_ratio*10),
    width = (PMZwidth - CEwidth)/2,
    height= PMZheight*mz_to_pmz_height_ratio*9,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(left_bottom)

    right_bottom = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength - PMZheight*mz_to_pmz_height_ratio*10),
    width = (PMZwidth - CEwidth)/2,
    height= PMZheight*mz_to_pmz_height_ratio*9,
    alpha= alpha,
    fc = 'k')
    ax.add_patch(right_bottom)

else:
    ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CMwidth/2.0,-PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,CEwidth/2.0,CMwidth/2.0,PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=alpha,linewidth=0)
    ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=alpha,linewidth=0)

if visualisationMode == 0:
    vor = Voronoi(data[nloop*nc:(nloop+1)*nc,1:3])
    regions, vertices = voronoi_finite_polygons_2d(vor,2)
    for j,region in enumerate(regions):
        polygon = vertices[region]
        ax.fill(polygon[:,1],polygon[:,0],color='grey',edgecolor='black',alpha=0.5)
    ax.scatter(data[nloop*nc:(nloop+1)*nc,2],data[nloop*nc:(nloop+1)*nc,1])
    ax.quiver(data[nloop*nc:(nloop+1)*nc,2],data[nloop*nc:(nloop+1)*nc,1],data[nloop*nc:(nloop+1)*nc,4],data[nloop*nc:(nloop+1)*nc,3],color="blue")
    ax.quiver(data[nloop*nc:(nloop+1)*nc,2],data[nloop*nc:(nloop+1)*nc,1],data[nloop*nc:(nloop+1)*nc,6],data[nloop*nc:(nloop+1)*nc,5],color="black")
    #tri = Delaunay(data[nloop*nc:(nloop+1)*nc,1:3])
    #plt.triplot(data[nloop*nc:(nloop+1)*nc,2], data[nloop*nc:(nloop+1)*nc,1], tri.simplices.copy(),color="black",alpha=0.5,ls="--")



elif visualisationMode == 1:
    #circles = [matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5, edgecolor="black",facecolor=color_list[ci]) for xi,yi,zi,ci in zip(data[nloop*nc:(nloop+1)*nc,2],data[nloop*nc:(nloop+1)*nc,1],data[nloop*nc:(nloop+1)*nc,7],data[nloop*nc:(nloop+1)*nc,9])]

    # Notochord outside chain zone
    # left_nc = matplotlib.patches.Rectangle((-2, -PMZheight/2 - Clength -PMZheight*2),
    #     width = 2 - CEwidth/2,
    #     height = PMZheight,
    #     alpha=alpha,
    #     fc= 'orchid')
    # ax.add_patch(left_nc)

    #Visualise just cells no boundary
    # big_patch = matplotlib.patches.Rectangle((-2, -PMZheight/2 - Clength -PMZheight*4),
    # width = 4,
    # height= 4,
    # alpha= alpha,
    # fc = 'k')
    # ax.add_patch(big_patch)

    outer_circles = [matplotlib.patches.Circle((xi,yi),alpha=0.5, radius=0.18,edgecolor="black",facecolor='lightskyblue') for xi,yi,zi,ci in zip(data[nloop*nc:(nloop+1)*nc,2],data[nloop*nc:(nloop+1)*nc,1],data[nloop*nc:(nloop+1)*nc,7],data[nloop*nc:(nloop+1)*nc,9])]
    for o_c in outer_circles:
        ax.add_patch(o_c)

    circles = [matplotlib.patches.Circle((xi,yi), radius=zi,edgecolor="black",facecolor=color_list[int(ci)]) for xi,yi,zi,ci in zip(data[nloop*nc:(nloop+1)*nc,2],data[nloop*nc:(nloop+1)*nc,1],data[nloop*nc:(nloop+1)*nc,7],data[nloop*nc:(nloop+1)*nc,9])]
    for c in circles:
        ax.add_patch(c)

# ax.set_xlim([-xmax,xmax])
# ax.set_ylim([-3*xmax/2-xmax*0.2,xmax/2-xmax*0.2])

ax.set_xlim([-xmax,xmax])
ax.set_ylim([-3*xmax/2-xmax*0.2,xmax/2-xmax*0.2])


fig.savefig(filepath+"/plot{:05d}.png".format(nloop),bbox_inches='tight',dpi=100,format='png')
ax.cla()
