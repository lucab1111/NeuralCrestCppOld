import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import pandas as pd
"""
Colors: PiYG, PRGn, BrBG, PuOr, RdGy, RdBu, RdBu, RdYlBu, RdYlBu, RdYlGn, Spectral, coolwarm, bwr, seismic
"""

# create an array of random vlues - you might read in a raster dataset
# x=20
# y=25

# elev_min=-1000
# elev_max=1000

# ras=np.random.randint(elev_min,elev_max,size=(x*y)).reshape(x,y)

data = pd.read_csv('all_sims_output.csv')
pivot = pd.pivot_table(data, index=["follower_De"], 
							columns=["leader_De"], 
							values = ["cells_out_mp"],
							aggfunc=np.mean)

# 
cmap=matplotlib.cm.YlGnBu # set the colormap to soemthing diverging

plt.xlabel('leader_De', fontsize = 12)
plt.ylabel('follower_De', fontsize = 12)
plt.title('Varying De between leaders and followers', fontsize = 12)


# norm = matplotlib.colors.Normalize(vmin=5, vmax=10)

plt.imshow(pivot, 
	cmap=cmap,
	interpolation='nearest',
	origin = 'lower',
	extent=[0.0001,0.001,0.0001,0.001])


#cbar = plt.colorbar(boundaries = [0,3])
cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 20
cbar.set_label('Mean number of MP passing cells', rotation=270, fontsize = 12)
#cbar.boundaries = [0,1]#(vmin=0, vmax=1)

#plt.show()

plt.savefig('heatmap.png')


