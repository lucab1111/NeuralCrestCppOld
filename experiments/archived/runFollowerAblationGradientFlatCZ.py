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

Nc = 7
zeta_mag = 0.005
cellradius = 0.13
PMZwidth = 1
PMZheight = 0.5
CEwidth = 0.4
CMwidth = CEwidth#*2.5#0.6
Clength = 1.4
t_max = 5000
dt = 0.1
output_interval = 200
chainShape = 0#1
realTimePlot = 1
experimentType = 14

leader_k = 0.01
leader_De = 0.5
leader_autonomousMag = 5e-8
leader_interactionThreshold = 2

follower_k = 0.01
follower_De = 0.5
follower_autonomousMag = 5e-9
follower_interactionThreshold = 1

for i in range(50):

    slurm_array_task = 1
    run = int(random.uniform(0,5000))
    gradientStrength = 0.0


    # Create the executable
    EXE = '/NeuralCrest {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
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
        leader_k,
        follower_De,
        follower_autonomousMag,
        follower_interactionThreshold,
        slurm_array_task,
        run,
        gradientStrength
        )


    completed_run = subprocess.run([EXE_DIR+EXE],
                                    shell=True,
                                    cwd= EXE_DIR)




