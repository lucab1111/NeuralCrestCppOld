import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay
from matplotlib.patches import Polygon
from math import sqrt
from sys import argv

visualisationMode = 1

# Read cell positions from file
data = np.genfromtxt(argv[1]+"/cellpositions.txt")
conditions = np.genfromtxt(argv[1]+"/initialconditions.txt")

nc = int(conditions[0,1]*3.0)
PMZwidth = conditions[7,1]
PMZheight = conditions[8,1]
CEwidth = conditions[9,1]
CMwidth = conditions[10,1]
Clength = conditions[11,1]
chainShape = conditions[15,1]

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
xmax=1.5   # Size of plots
Iterations = int(np.shape(data)[0]/nc)
fig,ax=plt.subplots()

for ii in range(Iterations):

    plt.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
    plt.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)
    ax.axis('equal')

    if visualisationMode == 0:
        vor = Voronoi(data[ii*nc:(ii+1)*nc,1:3])
        regions, vertices = voronoi_finite_polygons_2d(vor,2)
        for j,region in enumerate(regions):
            polygon = vertices[region]
            ax.fill(polygon[:,1],polygon[:,0],edgecolor='black',color='grey',alpha=0.5)
        ax.scatter(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1])
        ax.quiver(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,4],data[ii*nc:(ii+1)*nc,3],color="blue")
        ax.quiver(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,6],data[ii*nc:(ii+1)*nc,5],color="black")
        #tri = Delaunay(data[ii*nc:(ii+1)*nc,1:3])
        #plt.triplot(data[ii*nc:(ii+1)*nc,2], data[ii*nc:(ii+1)*nc,1], tri.simplices.copy(),color="black",alpha=0.5,ls="--")

    elif visualisationMode == 1:
        circles = [matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5,edgecolor="black") for xi,yi,zi in zip(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,7])]
        for c in circles:
            ax.add_patch(c)

    if chainShape==1:
        diamondOffset = (CMwidth-CEwidth)/2.0
        ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,CEwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,CEwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0],[diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0],[diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0],[-diamondOffset-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-diamondOffset-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    else:
        ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CMwidth/2.0,-PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,CEwidth/2.0,CMwidth/2.0,PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
        ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=0.5,linewidth=0)

    ax.set_xlim([-xmax,xmax])
    ax.set_ylim([-3*xmax/2-xmax*0.2,xmax/2-xmax*0.2])
    fig.savefig(argv[1]+"/plot{:05d}.png".format(ii),bbox_inches='tight',padding_inches=0,dpi=200,format='png')
    ax.cla()

os.system("convert -delay 10 -loop 0 "+argv[1]+"/plot*.png "+argv[1]+"/animated.gif")
