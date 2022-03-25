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


Nc = 7
zeta_mag = 0.007
cellradius = 0.13
PMZwidth = 1
PMZheight = 0.26 * 2
CEwidth = 0.4
CMwidth = CEwidth
Clength = 1
chainShape = 3
mz_pmz_ratio = 0.5

t_max = 20000
dt = 0.1
output_interval = 500

realTimePlot = 0
experimentType = 14

follower_k = 8.1e-04
follower_De = 8.1e-05
follower_autonomousMag = 5e-06
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = 1.11111e-07
leader_De = 8.1e-05
leader_autonomousMag = follower_autonomousMag
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = 0
leader_size = cellradius

granularity = 2

amaglist = np.linspace(follower_autonomousMag/2, follower_autonomousMag * 2, granularity)
Delist = np.linspace(follower_De*0.7, follower_De* 15, granularity)
klist = np.linspace(follower_k/ 15, follower_k*15, granularity)


for lk in klist:
    for fk in klist:

        for lDe in Delist:
            for fDe in Delist:

                for lamag in amaglist:
                    for famag in amaglist:

                        for i in range(30):

                            for ET in [17]:

                                slurm_array_task = 1
                                run = int(random.uniform(0,5000))


                                # Create the executable
                                EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
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
                                    run,
                                    mz_pmz_ratio
                                    )

                                print(EXE)


                                completed_run = subprocess.run([EXE_DIR+EXE],
                                                                shell=True,
                                                                cwd= EXE_DIR)




