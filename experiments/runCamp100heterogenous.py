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

leader_aMag_list = np.linspace(leader_autonomousMag, leader_autonomousMag * 27, granularity)
leader_k_list = np.linspace(leader_k, leader_k * max_multiple, granularity)
leader_De_list = np.linspace(leader_De, leader_De * max_multiple, granularity)

for i in range(5):

    for chainS in [3]:


        for laMag in leader_aMag_list:

            for lk in leader_k_list:

                for lDe in leader_De_list:

                    # Give followers level 1,2 and 3

                    for follower_level in range(granularity):

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
                                leader_k_list[follower_level],
                                leader_De_list[follower_level],
                                leader_aMag_list[follower_level],
                                follower_interactionThreshold,
                                follower_gradientSensitivity,
                                slurm_array_task,
                                run,
                                mz_pmz_ratio
                                )


                            completed_run = subprocess.run([OUTPUT_DIR+EXE],
                                                            shell=True,
                                                            cwd= OUTPUT_DIR)

                            # print('lk,' + str(lk))
                            # print('De,' + str(lDe))
                            # print('lamag,' + str(laMag))

                            # print('fk,' + str(leader_k_list[follower_level]))
                            # print('fDe,' + str(leader_De_list[follower_level]))
                            # print('faMag,' + str(leader_aMag_list[follower_level]))
