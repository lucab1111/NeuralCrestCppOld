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


Nc = 6
zeta_mag = 0.007 *5
cellradius = 0.13
PMZwidth = 1
PMZheight = 0.26 * 2
CEwidth = 0.4
CMwidth = CEwidth
Clength = 1
chainShape = 0
mz_pmz_ratio = 0.5

t_max = 2000
dt = 0.1
output_interval = 10

realTimePlot = 1

follower_k = 0.01
follower_De = 3e-05
follower_autonomousMag = 1.1e-07
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = 0.03
leader_De = 9e-05
leader_autonomousMag = 3e-06
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = 0
leader_size = cellradius


for i in range(1):


    for cew in [0.4]:

        for chainS in [3]:

            for ET in [1,]:# 2, 3, 5]:

                slurm_array_task = 1
                run = int(random.uniform(0,5000))


                # Create the executable
                EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
                    Nc,
                    zeta_mag,
                    cellradius,
                    PMZwidth,
                    PMZheight,
                    cew,
                    CMwidth,
                    Clength,
                    t_max,
                    dt,
                    output_interval,
                    chainS,
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
                    run,
                    mz_pmz_ratio
                    )

                print(EXE)


                completed_run = subprocess.run([EXE_DIR+EXE],
                                                shell=True,
                                                cwd= EXE_DIR)
