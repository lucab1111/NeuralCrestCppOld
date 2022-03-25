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

slurm_array_task = sys.argv[1]

# Path to executable
EXE_DIR = os.path.dirname(os.path.realpath(__file__)).replace('experiments','')

# Cell
Nc = 7
zeta_mag = 0.007
cellradius = 0.126

# Space
PMZwidth = 1
CEwidth = 0.41
CMwidth = CEwidth
PMZheight = 0.26*2
Clength = 1
chainShape = 1
middle_zone_ratio = 0.5

# Time
dt = 0.1
t_max = 5000
output_interval = 200

# Plot
realTimePlot = 0

# Heterogeneity

follower_k = 3e-5
follower_De = 8e-6
follower_autonomousMag = 8e-7/3
follower_interactionThreshold = 1
follower_gradientSensitivity = 0


leader_k = follower_k*5
leader_De = follower_De
leader_autonomousMag = follower_autonomousMag/2
leader_interactionThreshold = 1
leader_gradientSensitivity = 0
leader_size = cellradius#0.148

runMany = True

granularity = 3

#lamaglist = np.linspace(follower_autonomousMag, follower_autonomousMag * 3, granularity)
amaglist = np.linspace(follower_autonomousMag/2, follower_autonomousMag * 2, granularity)
Delist = np.linspace(follower_De*0.7, follower_De* 15, granularity)
klist = np.linspace(follower_k/ 15, follower_k*15, granularity)



for lk in klist:
    for fk in klist:

        for lDe in Delist:
            for fDe in Delist:

                for lamag in amaglist:
                    for famag in amaglist:

                        for ET in [17, 14, 19, 20]:#[17, 19, 20, 23, 14]:#, 19, 20]:#


                            for i in range(5):

                                run = int(random.uniform(0,10000))


                                # Create the executable
                                EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
                                    Nc,
                                    zeta_mag,
                                    cellradius,
                                    PMZwidth,
                                    PMZheight,
                                    CEwidth,    
                                    CMwidth,
                                    Clength -(PMZheight*middle_zone_ratio)/2,
                                    t_max,
                                    dt,
                                    output_interval,
                                    chainShape,
                                    realTimePlot,
                                    ET,
                                    lk,
                                    lDe,
                                    lamag,
                                    leader_interactionThreshold,
                                    leader_gradientSensitivity,
                                    leader_size,
                                    fk,
                                    fDe,
                                    famag,
                                    follower_interactionThreshold,
                                    follower_gradientSensitivity,
                                    slurm_array_task,
                                    run,
                                    middle_zone_ratio
                                    )

                                print(EXE)


                                completed_run = subprocess.run([EXE_DIR+EXE],
                                                                shell=True,
                                                                cwd= EXE_DIR)



