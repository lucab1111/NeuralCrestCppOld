import numpy as np
from os.path import join
import subprocess
import os
import shutil
import pandas as pd
import sys
"""
Generates the command line parameters for one simulation of the agent-based model, NeuralCrestCpp

Created: July 2020
Author: Dylan Feldner-Busztin
"""

slurm_array_task = sys.argv[1]

# Path to executable
EXE_DIR = os.path.dirname(os.path.realpath(__file__)).replace('experiments','')


def run_simulation(parameters):

    for experiment_type in [4]:

        Nc = 6
        k = 0.01
        De = 0.005
        zeta_mag = 0.01
        autonomousMag = 1e-09
        cellradius = 0.13
        interactionthreshold = 1
        PMZwidth = 1
        PMZheight = 0.5
        CEwidth = 0.45
        CMwidth = 0.6
        Clength = 1.4
        t_max = 5000
        dt = 0.1
        output_interval = 200
        chainShape = 0
        realTimePlot = 0
        experimentType = experiment_type
        leader_autonomousMag = parameters[0]
        leader_De = parameters[1]
        leader_interactionThreshold = parameters[2]
        follower_autonomousMag = parameters[3]
        follower_De = parameters[4]
        follower_interactionThreshold = parameters[5]

        for run in range(10):

            try:

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
                                                shell=True,
                                                cwd=EXE_DIR)

            except NotADirectoryError:
                print('Not Directory Error')
                pass
            except subprocess.TimeoutExpired:
                print('TimeoutExpired Error')
                pass

param_space_granularity = 10

# Use the paremeters that gave the optimal difference before
leader_aMag = 5e-09
leader_interactionThreshold = 1
follower_aMag = 5e-09
follower_interactionThreshold = 1


# Set boundaries
high_De = 0.1
low_De = 0.0001
De_options = [high_De, low_De]

follower_De_options = np.linspace(low_De, high_De, param_space_granularity)
leader_De_options = np.linspace(low_De, high_De, param_space_granularity)

for F_De in follower_De_options:
    for L_De in leader_De_options:

        combo = [leader_aMag, L_De, leader_interactionThreshold, 
        follower_aMag, F_De, follower_interactionThreshold]

        run_simulation(np.array(combo).flatten())



