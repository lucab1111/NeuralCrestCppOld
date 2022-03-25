import subprocess
import os
"""

Runs all the scores we'll want to show for the paper

"""

# Path to executable
PWD = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = PWD.replace('behaviour','')

# Archive results
EXE = "python3 archive_results.py"
create_output_dir = subprocess.run([EXE],
                            shell=True)

# Check final positions
#EXE = "python3 collect_final_y_positions.py " + OUTPUT_DIR + "output"
#EXE = "python3 collect_final_y_positions.py " + OUTPUT_DIR + "output_mar15_results_amag"
EXE = "python3 collect_final_y_positions.py " + OUTPUT_DIR + "output_mar15_results_k"
create_output_dir = subprocess.run([EXE],
                            shell=True)

# Check overtakes
EXE = 'python3 iterate_over_simulations.py'
print(EXE)
create_output_dir = subprocess.run([EXE],
                            shell=True)