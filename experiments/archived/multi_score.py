import numpy as np
from os.path import join
import subprocess
import os
import shutil
import pandas as pd
import sys
import random
"""
Generates the command line parameters for one simulation of the agent-based model, NeuralCrestCpp

Created: August 2020
Author: Dylan Feldner-Busztin
"""

# Path to executable
EXE_DIR = os.path.dirname(os.path.realpath(__file__)).replace('experiments','')


Nc = 6
zeta_mag = 0.005
cellradius = 0.13
PMZwidth = 1
PMZheight = 0.5
CEwidth = 0.4
CMwidth = CEwidth#*2.5#0.6
Clength = 1.4
t_max = 80000
dt = 0.1
output_interval = 500
chainShape = 1
realTimePlot = 0
#experimentType = 14

leader_k = 0.001
leader_De = 0.0005#0.0005
leader_autonomousMag = 5e-9#5e-8
leader_interactionThreshold = 1
leader_gradientSensitivity = 0.005
leader_size = cellradius/2.0

follower_k = 0.001
follower_De = 0.0005#0.0001
follower_autonomousMag = 5e-9
follower_interactionThreshold = 1
follower_gradientSensitivity = 0.0001

for expType in [12, 14, 15, 18]:#[14, 15, 18]: # 14 is control, 15 is follower ablation, 18 is leader ablation, 
    
    for leaderSize in [0.03, 0.05, 0.07, 0.09, 0.11, 0.13]:

        for leaderGrad in [ 0.000001 , 0.001, 0.002, 0.003, 0.004, 0.005 ]:

            for i in range(2):

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
                    expType,
                    leader_k,
                    leader_De,
                    leader_autonomousMag,
                    leader_interactionThreshold,
                    leader_gradientSensitivity,
                    leaderSize,
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




