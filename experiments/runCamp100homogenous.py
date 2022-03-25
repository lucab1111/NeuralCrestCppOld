import subprocess
import random
import os
import numpy as np
import sys

# Path to executable
PWD = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = PWD.replace('experiments','')

slurm_array_task = sys.argv[1]

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

realTimePlot = 0

follower_k = 0.01
follower_De = 0.00003
follower_autonomousMag = 1e-6 / 9 # max will now be x3 x3 x3
follower_interactionThreshold = 1
follower_gradientSensitivity = 0

leader_k = follower_k# * 1.5
leader_De = follower_De
leader_autonomousMag = follower_autonomousMag
leader_interactionThreshold = follower_interactionThreshold
leader_gradientSensitivity = follower_gradientSensitivity
leader_size = cellradius

granularity = 3
max_multiple = 3

for i in range(10):

    for chainS in [3]:


        for laMag in np.linspace(leader_autonomousMag, leader_autonomousMag * 27, granularity):

            for lk in np.linspace(leader_k, leader_k * max_multiple, granularity):

                for lDe in np.linspace(leader_De, leader_De * max_multiple, granularity):



                    for ET in [4, 8, 1,2,3,7]:

                        #slurm_array_task = 1
                        run = int(random.uniform(0,1e6))


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
                            lk,
                            lDe,
                            laMag,
                            leader_interactionThreshold,
                            leader_gradientSensitivity,
                            leader_size,
                            lk,
                            lDe,
                            laMag,
                            follower_interactionThreshold,
                            follower_gradientSensitivity,
                            slurm_array_task,
                            run,
                            mz_pmz_ratio
                            )


                        completed_run = subprocess.run([OUTPUT_DIR+EXE],
                                                        shell=True,
                                                        cwd= OUTPUT_DIR)

                        # print(lk)
                        # print(lDe)
                        # print(laMag)


# # Check final positions
# EXE = "python3 collect_final_y_positions.py " + OUTPUT_DIR + "output"
# print(EXE)
# collect_finalys = subprocess.run([EXE],
#                             shell=True)

# # Check overtakes
# EXE = 'python3 iterate_over_simulations.py'
# print(EXE)
# iterated_sims = subprocess.run([EXE],
#                             shell=True)