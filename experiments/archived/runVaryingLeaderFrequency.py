import numpy as np
from os.path import join
import subprocess
import os
import shutil
import pandas as pd
import sys
import random
"""
Generates the command line parameters and runs the agent-based model, NeuralCrestCpp

Created: August 2020
Author: Dylan Feldner-Busztin
"""

# Path to executable
EXE_DIR = os.path.dirname(os.path.realpath(__file__)).replace('experiments','')


Nc = 5
zeta_mag = 0.01
cellradius = 0.13
PMZwidth = 1
PMZheight = 0.4
CEwidth = 0.4
CMwidth = CEwidth#*10#0.6
Clength = 0.8
t_max = 20000
dt = 0.1
output_interval = 100
chainShape = 2
realTimePlot = 1
experimentType = 14

follower_k = 0.0005
follower_De = 0.0005*3
follower_autonomousMag = 15e-7/3.0 *2
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = follower_k
leader_De = follower_De
leader_autonomousMag = follower_autonomousMag*3*2*2
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = 0.002
leader_size = cellradius/2.0


for ET in [12]:#, 5, 6]:#[17, 4, 19, 20, 12, 13]:

    for i in range(3):

    

        slurm_array_task = 1
        run = int(random.uniform(0,5000))


        # Create the executable
        EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
            Nc,
            zeta_mag,
            cellradius,
            PMZwidth,
            PMZheight,
            CEwidth,
            CMwidth,
            Clength,
            t_max,
            dt,
            output_interval,
            chainShape,
            realTimePlot,
            ET,
            leader_k,
            leader_De,
            leader_autonomousMag,
            leader_interactionThreshold,
            leader_gradientSensitivity,
            leader_size,
            follower_k,
            follower_De,
            follower_autonomousMag,
            follower_interactionThreshold,
            follower_gradientSensitivity,
            slurm_array_task,
            run
            )

        print(EXE)


        completed_run = subprocess.run([EXE_DIR+EXE],
                                        shell=True,
                                        cwd= EXE_DIR)




