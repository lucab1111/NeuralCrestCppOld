import os
import subprocess
import time
"""

Moves previous results and renames them according to the current time

"""

# Path to executable
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Check if there already an output file
finpos_file_exists = os.path.isfile('final_position_results.csv')

# Use current date/time for the naming
new_name_output = 'final_position_results_' + time.strftime("%Y_%m_%d_%H_%M_%S")

if finpos_file_exists:

    # Change the name to output + current date/time
    EXE = 'mv final_position_results.csv archived/{}'.format(new_name_output)
    change_output_name = subprocess.run([EXE],
                                shell=True,
                                cwd= CURRENT_DIR)

# Check if there already an output file
overtakes_file_exists = os.path.isfile('overtake_counts_.csv')

# Use current date/time for the naming
new_name_output = 'overtakes_results_' + time.strftime("%Y_%m_%d_%H_%M_%S")

if overtakes_file_exists:

    # Change the name to output + current date/time
    EXE = 'mv overtake_counts_.csv archived/{}'.format(new_name_output)
    change_output_name = subprocess.run([EXE],
                                shell=True,
                                cwd= CURRENT_DIR)