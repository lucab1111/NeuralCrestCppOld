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
Nc = 4
zeta_mag = 0.007
cellradius = 0.13

# Space
PMZwidth = 1
CEwidth = 0.4
CMwidth = CEwidth
PMZheight = 0.26*2
Clength = 1
chainShape = 3

# Time
dt = 0.1
t_max = 600
dt = 0.1
output_interval = 10

# Plot
realTimePlot = 0

# Heterogeneity

follower_k = 0.000003
follower_De = 8.1e-05
follower_autonomousMag = 5e-06
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = follower_k
leader_De = 9e-06
leader_autonomousMag = 1e-07 * 9
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = 0.1
leader_size = cellradius

runMany = True

granularity = 3

#lamaglist = np.linspace(follower_autonomousMag, follower_autonomousMag * 3, granularity)
amaglist = np.linspace(follower_autonomousMag/2, follower_autonomousMag * 2, 3)
Delist = np.linspace(follower_De, follower_De* 9, 3)
klist = np.linspace(follower_k/ 9, follower_k*9, granularity)

ncellslist = [5, 6, 7]
mzlist = [0.6, 1, 0.8]
lgrad = [0.3,1,0.6]
cwlist = [0.36, 0.34, 0.42]


if runMany == True:

    for lamag in amaglist:
        for famag in amaglist:#amaglist:

            for lDe in Delist:#Delist:
                for fDe in Delist: #Delist:

                    for lk in klist:
                        for fk in klist:

                            for ncells in ncellslist:
                                for mz in mzlist:

                                    for lg in lgrad:

                                        for cw in cwlist:

                                            for i in range(20):

                                                for ET in [17, 19, 20, 23]:#

                                                    #slurm_array_task = 1
                                                    run = int(random.uniform(0,5000))


                                                    # Create the executable
                                                    EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
                                                        ncells,
                                                        zeta_mag,
                                                        cellradius,
                                                        PMZwidth,
                                                        PMZheight,
                                                        cw,    
                                                        CMwidth,
                                                        Clength -(PMZheight*mz)/2,
                                                        t_max,
                                                        dt,
                                                        output_interval,
                                                        chainShape,
                                                        realTimePlot,
                                                        ET,
                                                        follower_k,
                                                        lDe,
                                                        lamag,
                                                        leader_interactionThreshold,
                                                        lg,
                                                        leader_size,
                                                        follower_k,
                                                        fDe,
                                                        famag,
                                                        follower_interactionThreshold,
                                                        follower_gradientSensitivity,
                                                        slurm_array_task,
                                                        run,
                                                        mz
                                                        )

                                                    print(EXE)


                                                    completed_run = subprocess.run([EXE_DIR+EXE],
                                                                                    shell=True,
                                                                                    cwd= EXE_DIR)


else:


    for lamag in lamaglist:

        for fDe in fDelist:

            for lk in lklist:


                for ET in [19, 20, 25, 23]:#

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
                        1,
                        ET,
                        lk,
                        fDe,
                        lamag,
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
                        middle_zone_space
                        )

                    print(EXE)


                    completed_run = subprocess.run([EXE_DIR+EXE],
                                                    shell=True,
                                                    cwd= EXE_DIR)

