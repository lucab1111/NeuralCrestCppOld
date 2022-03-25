import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay
from matplotlib.patches import Polygon
from math import sqrt
from sys import argv
import pandas as pd
import os



visualisationMode = 1

# Read cell positions from file
data = np.genfromtxt(argv[1]+"/cellpositions.txt")

cellpositions_df = pd.read_csv(argv[1] + os.sep + 'cellpositions.txt',
                    sep = ' ',
                    header=None)


cellpositions_df.columns = ['Time',
                            'Y_microns',
                            'X_microns',
                            'v_auto_0',
                            'v_auto_1',
                            'v_bound_0',
                            'v_bound_1',
                            'cellradius',
                            'ListName',
                            'cell_type',
                            'notch',
                            'dll4',
                            'experiment_type',
                            'Nc']


initial_conditions = pd.read_csv(argv[1]+'/initialconditions.txt',header=None,delimiter=r"\s+")
initial_conditions.columns = ['Parameter','Value']

nc = int(initial_conditions.loc[initial_conditions['Parameter']=='Nc'].values[0][1]*3.0)
PMZwidth = initial_conditions.loc[initial_conditions['Parameter']=='PMZwidth'].values[0][1]
PMZheight = initial_conditions.loc[initial_conditions['Parameter']=='PMZheight'].values[0][1]
Clength = initial_conditions.loc[initial_conditions['Parameter']=='Clength'].values[0][1]
CMwidth = initial_conditions.loc[initial_conditions['Parameter']=='CMwidth'].values[0][1]
CEwidth = initial_conditions.loc[initial_conditions['Parameter']=='CEwidth'].values[0][1]
chainShape = initial_conditions.loc[initial_conditions['Parameter']=='chainShape'].values[0][1]

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
color_list = [(0.8313725490196079, 0.8313725490196079, 0.8313725490196079, 1.0),
            (0.23529411764705882, 0.7333333333333333, 0.7294117647058823, 1.0),
            (0.5372549019607843, 0.16862745098039217, 0.4196078431372549, 1.0)]
xmax=1.5   # Size of plots
#Iterations = int(np.shape(data)[0]/nc)
#Iterations = int(np.shape(data)[0]/max(cellpositions_df.Time))

timeStepList = cellpositions_df.Time.unique()
Iterations = len(timeStepList)

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
        #circles = [matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5,edgecolor="black", facecolor="red") for xi,yi,zi in zip(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,7])]
        #circles = [matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5,edgecolor="black",facecolor=color_list[int(ci)]) for xi,yi,zi,ci in zip(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,7],data[ii*nc:(ii+1)*nc,9])]

        timeStep = timeStepList[ii]
        timeframe = cellpositions_df.query('Time == @timeStep')

        for index, row in timeframe.iterrows():

            xi = row['X_microns']
            yi = row['Y_microns']
            zi = row['cellradius']
            ci = row['cell_type']
            # previous_X = row['previous_X_microns']
            # previous_Y = row['previous_Y_microns']

            circle = matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5,edgecolor="black",facecolor=color_list[int(ci)])
            ax.add_patch(circle)

            # arrow = matplotlib.patches.FancyArrow(xi, yi, xi-previous_X, yi-previous_Y, width=0.001,head_length=0.08, head_width=0.08, capstyle='butt')
            # ax.add_patch(arrow)

        # circles = [matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5,edgecolor="black",facecolor=color_list[int(ci)]) for xi,yi,zi,ci in zip(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,7],data[ii*nc:(ii+1)*nc,9])]
        # for c in circles:
        #     ax.add_patch(c)




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
    fig.savefig(argv[1]+"/plot{:05d}.png".format(ii),bbox_inches='tight',dpi=200,format='png')
    ax.cla()

os.system("convert -delay 10 -loop 0 "+argv[1]+"/plot*.png "+argv[1]+"/animated.gif")
