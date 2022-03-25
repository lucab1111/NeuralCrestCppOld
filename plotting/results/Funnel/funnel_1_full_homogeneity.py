import plotly.express as px
import pandas as pd


stages = [  "All parameter combinations", 
            "Maximum distance between migrating cells < 57 microns",
            "80 percent single-file time steps on average",
            "Average follower overtakes > 1 per run",
            "Average leader overtakes < 0.1 per run",
            "Average ventral distance ~120 microns",
            "Homogenous system has more leader overtakes than heterogenous system",
            "Heterogenous system descends further than homogenous system",
            "All leaders descend further than all followers"]

df = pd.DataFrame(dict(number=[27, 
                                25,
                                24,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0], 
                        stage=stages))

df['Simulation scores'] = '100 runs each'

fig = px.funnel(df, 
                x='number', 
                y='stage', 
                color='Simulation scores')

fig.update_layout(title='Possible Parameter Combinations: Every Fourth Cell Is A leader', 
                font=dict(size=30))


fig.write_image("funnel1.png")

fig.show()