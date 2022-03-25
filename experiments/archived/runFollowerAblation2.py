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


EXE_DIR = os.path.dirname(os.path.realpath(__file__)).replace('experiments','')

for run_id in range(1):


    Nc = 7
    zeta_mag = 0.01
    autonomousMag = 1e-09
    cellradius = 0.13
    interactionthreshold = 1
    PMZwidth = 1
    PMZheight = 0.5
    CEwidth = 0.3#0.45
    CMwidth = CEwidth*3#0.6
    Clength = 1.4
    t_max = 5000
    dt = 0.1
    output_interval = 200
    chainShape = 1
    realTimePlot = 0
    experimentType = sys.argv[1] # 5 Is regular, 4 is control, 7 is next leader

    leader_k = 0.001
    leader_De = 0.01
    leader_autonomousMag = 5e-08
    leader_interactionThreshold = 1

    follower_k = 0.005
    follower_De = 0.08
    follower_autonomousMag = 5e-09
    follower_interactionThreshold = 1

    slurm_array_task = 1
    run = int(random.uniform(0,10000))

            # Create the executable
    EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
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
        experimentType,

        leader_k,
        leader_De,
        leader_autonomousMag,
        leader_interactionThreshold,

        follower_k,
        follower_De, 
        follower_autonomousMag,
        follower_interactionThreshold,

        slurm_array_task,
        run
        )

    print(EXE)


    # Run the simulation
    completed_run = subprocess.run([EXE_DIR+EXE], 
                                    shell = True,
                                    cwd= EXE_DIR)





