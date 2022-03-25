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


Nc = 6
zeta_mag = 0.003
cellradius = 0.13
PMZwidth = 1
PMZheight = 0.4
CEwidth = 0.4
CMwidth = CEwidth
Clength = 0.8
t_max = 50000
dt = 0.1
output_interval = 500
chainShape = 2
realTimePlot = 0
experimentType = 14

follower_k = 0.000003
follower_De = 3e-06
follower_autonomousMag = 5e-07 * 3
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = follower_k 
leader_De = 9e-06
leader_autonomousMag = 1e-07 * 3
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = 0
leader_size = cellradius

runMany = True

lamaglist = np.linspace(follower_autonomousMag/ 27, follower_autonomousMag * 27, 5)
fDelist = np.linspace(follower_De/ 27, follower_De* 27, 5)
intThreshlist = np.linspace(1, 2, 5)
lklist = np.linspace(follower_k/ 27, follower_k*27, 5)


if runMany == True:

    for i in range(1):

        for lamag in lamaglist:

            for fDe in fDelist:

                for intThr in intThreshlist:

                    for lk in lklist:


                        for ET in [23, 17]:#

                            #slurm_array_task = 1
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
                                lk,
                                leader_De,
                                lamag,
                                intThr,
                                leader_gradientSensitivity,
                                leader_size,
                                follower_k,
                                fDe,
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


else:

                    for ET in [23]:

                        for lgrad in [0.12]:

                            for i in range(1):

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
                                    1,
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

