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

for run_id in range(500):


    Nc = 6
    k = 0.01
    De = 0.005
    zeta_mag = 0.01
    autonomousMag = 1e-09
    cellradius = 0.13
    interactionthreshold = 1
    PMZwidth = 1
    PMZheight = 0.5
    CEwidth = 0.3
    CMwidth = 0.8
    Clength = 1.4
    t_max = 5000
    dt = 0.1
    output_interval = 200
    chainShape = 1
    realTimePlot = 0
    experimentType = 6
    leader_autonomousMag = 5e-08
    leader_De = 0.02
    leader_interactionThreshold = 2
    follower_autonomousMag = 5e-08
    follower_De = 0.08
    follower_interactionThreshold = 2
    slurm_array_task = 1
    run = run_id

            # Create the executable
    EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
        Nc,
        k,
        De,
        zeta_mag,
        autonomousMag,
        cellradius,
        interactionthreshold,
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
        leader_autonomousMag,
        leader_De,
        leader_interactionThreshold,
        follower_autonomousMag,
        follower_De,
        follower_interactionThreshold,
        slurm_array_task,
        run
        )


    # Run the simulation
    completed_run = subprocess.run([EXE_DIR+EXE], 
                                    shell = True,
                                    cwd= EXE_DIR)





