import subprocess
import time
import os
import random
import pandas as pd

# current

# Path to executable
PWD = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = PWD.replace('experiments','')

# Use current date/time for the naming
new_name_output = 'output_' + time.strftime("%Y_%m_%d_%H_%M_%S")

# Check if there already an output file
output_dir_exists = os.path.isdir(OUTPUT_DIR + 'output')

if output_dir_exists:

    # Change the name to output + current date/time
    EXE = 'mv output archived_outputs/{}'.format(new_name_output)
    change_output_name = subprocess.run([EXE],
                                shell=True,
                                cwd= OUTPUT_DIR)

    # Create a new output directory
    EXE = 'mkdir output'
    create_output_dir = subprocess.run([EXE],
                                shell=True,
                                cwd= OUTPUT_DIR)

else: 

    # Create a new output directory
    EXE = 'mkdir output'
    create_output_dir = subprocess.run([EXE],
                                shell=True,
                                cwd= OUTPUT_DIR)

# # Compile
# EXE = 'make clean; make'
# make_clean_make = subprocess.run([EXE],
#                             shell=True,
#                             cwd= OUTPUT_DIR)



Nc = 7
zeta_mag = 0.007 * 7
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

realTimePlot = 0

follower_k = 0.01
follower_De = 0.00003
follower_autonomousMag = 1e-6
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = follower_k * 2
leader_De = follower_De
leader_autonomousMag = follower_autonomousMag
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = follower_gradientSensitivity
leader_size = cellradius

for i in range(1):

    for chainS in [3]:

        for ET in [2,3,7]:

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


            completed_run = subprocess.run([OUTPUT_DIR+EXE],
                                            shell=True,
                                            cwd= OUTPUT_DIR)
