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

alpha = 1

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
mz_to_pmz_height_ratio = initial_conditions.loc[initial_conditions['Parameter']=='middle_zone_height'].values[0][1]
cellradius = initial_conditions.loc[initial_conditions['Parameter']=='cellradius'].values[0][1]


# Determine which is the first cell out

for index, row in cellpositions_df.iterrows():

    cell_y = row['Y_microns']
    cell_type = row['cell_type']
    transistion_time = row['Time']

    if cell_y < -PMZheight/2.0-Clength/10.0 and cell_type == 2:

        first_cell_out_ID = row['ListName']
        break

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
# color_list = [(0.8313725490196079, 0.8313725490196079, 0.8313725490196079, 1.0),
#             (0.23529411764705882, 0.7333333333333333, 0.7294117647058823, 1.0),
#             (0.5372549019607843, 0.16862745098039217, 0.4196078431372549, 1.0)]

color_list = [(0.8313725490196079, 0.8313725490196079, 0.8313725490196079, 1.0),
            (90/255, 195/255, 195/255, 1.0),
            (143/255, 48/255, 120/255, 1.0)]

xmax=1.5   # Size of plots

timeStepList = cellpositions_df.Time.unique()
Iterations = len(timeStepList)

fig,ax=plt.subplots()

for ii in range(Iterations):

    plt.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
    plt.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)
    ax.axis('equal')

    if chainShape==1 or chainShape == 0:
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

    if chainShape == 2:
        # Top strip
        ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],
            c="Black",
            alpha=alpha,
            linewidth=0)
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
        fc = 'k',
        edgecolor='k')
        ax.add_patch(left_top)

        right_top = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength),
        width = (PMZwidth - CEwidth)/2,
        height= Clength,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(right_top)

        left_bottom = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength - PMZheight*4),
        width = (PMZwidth - CEwidth)/2,
        height= PMZheight*3,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(left_bottom)

        right_bottom = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength - PMZheight*4),
        width = (PMZwidth - CEwidth)/2,
        height= PMZheight*3,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(right_bottom)

        middle_zone_border = - PMZheight/2 - Clength - PMZheight

        x = [-3,3]
        y = [middle_zone_border,middle_zone_border]

        #dashes = [5,2,10,5] # 5 points on, 2 off, 3 on, 1 off

        #l, = plt.plot(x,y, '--')

    if chainShape == 3:


        # Left strip
        ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],
            c="Black",
            alpha=alpha,
            ec = 'k',
            linewidth=0)

        # Right strip
        ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],
            c="Black",
            alpha=alpha,
            ec = 'k',
            linewidth=0)

        # Top strip
        top_strip = matplotlib.patches.Rectangle((-PMZwidth*4, PMZheight/2),
        width = PMZwidth*8,
        height= PMZheight,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(top_strip)

        # Add four grey squares around MiddleZone

        left_top = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength),
        width = (PMZwidth - CEwidth)/2,
        height= Clength,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(left_top)

        right_top = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength),
        width = (PMZwidth - CEwidth)/2,
        height= Clength,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(right_top)

        left_bottom = matplotlib.patches.Rectangle((-PMZwidth/2, -PMZheight/2 - Clength - PMZheight*mz_to_pmz_height_ratio*10),
        width = (PMZwidth - CEwidth)/2,
        height= PMZheight*mz_to_pmz_height_ratio*9,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(left_bottom)

        right_bottom = matplotlib.patches.Rectangle((PMZwidth/2 - (PMZwidth - CEwidth)/2, -PMZheight/2 - Clength - PMZheight*mz_to_pmz_height_ratio*10),
        width = (PMZwidth - CEwidth)/2,
        height= PMZheight*mz_to_pmz_height_ratio*9,
        alpha= alpha,
        edgecolor='k',
        fc = 'k')
        ax.add_patch(right_bottom)

        #data['lowest_y'] > -data['PMZheight']/2 - (Clength-(data['PMZheight']*data['middle_zone_height'])/2) - data['middle_zone_height']

        middle_zone_border = -PMZheight/2  -(Clength) -(PMZheight*mz_to_pmz_height_ratio)

        # x = [-3,3]
        # y = [middle_zone_border,middle_zone_border]

        # #dashes = [5,2,10,5] # 5 points on, 2 off, 3 on, 1 off

        # l, = plt.plot(x,y, '--', c = 'b') 

        # outer_threshold = middle_zone_border - cellradius*4
        # print(outer_threshold)

        # x2 = [-3,3]
        # y2 = [outer_threshold,outer_threshold]

        # #dashes = [5,2,10,5] # 5 points on, 2 off, 3 on, 1 off

        # l2, = plt.plot(x2,y2, '--', c = 'r') 



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
            ID = row['ListName']
            time = row['Time']
            # previous_X = row['previous_X_microns']
            # previous_Y = row['previous_Y_microns']

            # if ID == first_cell_out_ID and time >= transistion_time:

            #     circle = matplotlib.patches.Circle((xi,yi), radius=zi/2, alpha=alpha,edgecolor="black",facecolor='y')
            #     ax.add_patch(circle)
            #     # print('Leader_cell')
            #     # print(first_cell_out_ID)

            circle = matplotlib.patches.Circle((xi,yi), radius=zi, alpha=alpha,edgecolor="black",facecolor=color_list[int(ci)])
            ax.add_patch(circle)




            # arrow = matplotlib.patches.FancyArrow(xi, yi, xi-previous_X, yi-previous_Y, width=0.001,head_length=0.08, head_width=0.08, capstyle='butt')
            # ax.add_patch(arrow)

        # circles = [matplotlib.patches.Circle((xi,yi), radius=zi, alpha=0.5,edgecolor="black",facecolor=color_list[int(ci)]) for xi,yi,zi,ci in zip(data[ii*nc:(ii+1)*nc,2],data[ii*nc:(ii+1)*nc,1],data[ii*nc:(ii+1)*nc,7],data[ii*nc:(ii+1)*nc,9])]
        # for c in circles:
        #     ax.add_patch(c)

    # else:
    #     ax.fill([5,-5,-PMZheight/2.0,PMZheight/2.0],[PMZheight/2.0,PMZheight/2.0,5,5],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([PMZwidth/2.0,PMZwidth/2.0,5,5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([-PMZwidth/2.0,-PMZwidth/2.0,-5,-5],[PMZheight/2.0,-5,-PMZheight/2.0,PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([-PMZwidth/2.0,-CEwidth/2.0,-CMwidth/2.0,-PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([PMZwidth/2.0,CEwidth/2.0,CMwidth/2.0,PMZwidth/2.0],[-PMZheight/2.0,-PMZheight/2.0,-Clength-PMZheight/2.0,-Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([-PMZwidth/2.0,-CMwidth/2.0,-CEwidth/2.0,-PMZwidth/2.0],[-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([PMZwidth/2.0,CMwidth/2.0,CEwidth/2.0,PMZwidth/2.0],[-Clength-PMZheight/2.0,-Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0],c="Black",alpha=0.5,linewidth=0)
    #     ax.fill([-PMZwidth/2.0,PMZwidth/2.0,PMZwidth/2.0,-PMZwidth/2.0],[-2.0*Clength-PMZheight/2.0,-2.0*Clength-PMZheight/2.0,-5.0,-5.0],c="Black",alpha=0.5,linewidth=0)

    # ax.set_xlim([-xmax,xmax])
    # ax.set_ylim([-3*xmax/2-xmax*0.2,xmax/2-xmax*0.2])

    ax.set_xlim([-xmax,xmax])
    ax.set_ylim([-3*xmax/2-xmax*0.2 +0.15,xmax/2-xmax*0.2])


    fig.savefig(argv[1]+"/plot{:05d}.png".format(ii),bbox_inches='tight',dpi=400,format='png')
    ax.cla()

os.system("convert -delay 10 -loop 0 "+argv[1]+"/plot*.png "+argv[1]+"/animated.gif")