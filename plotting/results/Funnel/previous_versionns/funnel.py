import plotly.express as px
import pandas as pd


stages = [  "All parameter combinations", 
			"Max distance between migrating cells < 45 microns",
		    "80 percent single-file time steps on average",
		    "Average follower overtakes > 0.2 per run",
		    "Average leader overtakes < 0.1 per run",
		    "Average vertical distance > 115 microns",
		    "Heterogenous system descend further than homogenous system"]

df = pd.DataFrame(dict(number=[27, 
								24,
								24,
								17,
								14,
								14,
								14], 
						stage=stages))

df['Simulation scores'] = '50 runs each'

fig = px.funnel(df, 
				x='number', 
				y='stage', 
				color='Simulation scores')

fig.update_layout(title='Every odd cell a leader', 
				font=dict(size=30))


fig.write_image("odd_cell_leader.png")

fig.show()