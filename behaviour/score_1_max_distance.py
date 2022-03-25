import pandas as pd
import numpy as np
import sys
import os
from sys import argv
import math
pd.options.mode.chained_assignment = None  # default='warn'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

"""
Calculate max distance between migrating cells.

Usage: must be run after score_0_preprocessing is completed.

"""

# Must be run from within behaviour
#OUTPUT_DIRECTORY = '../test_leader_overtakes_1' #'output'
OUTPUT_DIRECTORY = '../output'
#OUTPUT_DIRECTORY = '/Users/feldnerd/Documents/GitHub/NeuralCrestCpp/test_leader_overtakes_2'#argv[1]

print(OUTPUT_DIRECTORY)

BATCH_PROCESSING_FLAG = 0
NUMBER_BUCKETS = 45
ARRAY_INDEX = argv[1]

file_list = [file[0] for file in os.walk(OUTPUT_DIRECTORY)]

# If BATCH_PROCESSING_FLAG is 1 then split the data up for parallel processing
if int(BATCH_PROCESSING_FLAG) == 1:
    # Focus on subsection of file_list
    number_of_files = len(file_list)
    number_of_buckets = int(NUMBER_BUCKETS)
    approx_files_per_bucket = int(number_of_files / number_of_buckets)
    lower_bound = int(ARRAY_INDEX) * approx_files_per_bucket
    upper_bound = lower_bound + approx_files_per_bucket
    file_list = file_list[lower_bound:upper_bound]

result_df = pd.DataFrame()


def max_intercell_distances(cell_position_df, PMZheight, Clength):

    neighbour_distances = []

    if len(cell_position_df.index) > 0:

        # Threshold outside PMZ
        defined_as_migrating = -PMZheight/2 - Clength/10
        migrating_cells_df = cell_position_df.query("Y_microns < @defined_as_migrating")

        # Rank cells
        rank_series = migrating_cells_df.groupby('Time')['Y_microns'].rank()
        migrating_cells_df = migrating_cells_df.assign(rank=rank_series)

        list_time_steps = migrating_cells_df.Time.unique()

        if len(list_time_steps) == 0:
            neighbour_distances = [0]

        for time_step in range(len(list_time_steps)):

            if time_step > 0:

                this_time_step_df = migrating_cells_df[migrating_cells_df['Time'] == list_time_steps[time_step]]

                # Order df by height
                this_time_step_df = this_time_step_df.sort_values('Y_microns')

                prev_x = np.nan
                prev_y = np.nan

                for index, row in this_time_step_df.iterrows():

                    this_x = row['X_microns']
                    this_y = row['Y_microns']

                    #print(this_y)

                    if np.isnan(prev_x) and np.isnan(prev_y): # First cell

                        prev_x = this_x
                        prev_y = this_y
                        continue

                    else:

                        inter_cell_distance = math.sqrt( math.pow((prev_y - this_y), 2) +  math.pow((prev_x - this_x), 2 ) )
                        neighbour_distances.append(inter_cell_distance)

                        this_cell = row['ListName']
                        prev_cell = this_time_step_df[this_time_step_df['Y_microns'] == prev_y].ListName.values[0]

                        # if inter_cell_distance > threshold:
                        #         print('#At time ' + str(time_step) + ' Distance between cell ' + str(this_cell) + ' and ' + str(prev_cell) + ' is ' + str(inter_cell_distance))

                    prev_x = this_x
                    prev_y = this_y

    if len(neighbour_distances) > 0:
    	return max(neighbour_distances)

    else:
    	return 'NaN'


# Loop through all files and get a table of results
for file_index in range(len(file_list)):

    filename = file_list[file_index]
    print(filename)

    if filename != OUTPUT_DIRECTORY:

        if os.path.isfile(filename+'/initialconditions.txt'):

            try:

                # Get df of initial conditions
                initial_conditions = pd.read_csv(filename+'/initialconditions.txt',header=None,delimiter=r"\s+")
                initial_conditions.columns = ['Parameter','Value']

                if not len(initial_conditions) == 28:
                    print("Initial conditions incomplete")

                else:

                    # Extract relevant information about the run
                    follower_k = initial_conditions.loc[initial_conditions['Parameter']=='follower_k'].values[0][1]
                    follower_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='follower_autonomousMag'].values[0][1]
                    follower_De = initial_conditions.loc[initial_conditions['Parameter']=='follower_De'].values[0][1]

                    leader_k = initial_conditions.loc[initial_conditions['Parameter']=='leader_k'].values[0][1]
                    leader_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='leader_autonomousMag'].values[0][1]
                    leader_De = initial_conditions.loc[initial_conditions['Parameter']=='leader_De'].values[0][1]

                    experimentType = initial_conditions.loc[initial_conditions['Parameter']=='experimentType'].values[0][1]
                    PMZheight = initial_conditions.loc[initial_conditions['Parameter']=='PMZheight'].values[0][1]
                    PMZwidth = initial_conditions.loc[initial_conditions['Parameter']=='PMZwidth'].values[0][1]
                    Clength = initial_conditions.loc[initial_conditions['Parameter']=='Clength'].values[0][1]
                    CEwidth = initial_conditions.loc[initial_conditions['Parameter']=='CEwidth'].values[0][1]
                    migratory_zone_border = -PMZheight/2.0 -Clength/10.0
                    Ncells = initial_conditions.loc[initial_conditions['Parameter']=='Nc'].values[0][1]
                    middle_zone_height = initial_conditions.loc[initial_conditions['Parameter']=='middle_zone_height'].values[0][1]
                    lgrad = initial_conditions.loc[initial_conditions['Parameter']=='leader_gradientSensitivity'].values[0][1]
                    fgrad = initial_conditions.loc[initial_conditions['Parameter']=='follower_gradientSensitivity'].values[0][1]
                    chainShape = initial_conditions.loc[initial_conditions['Parameter']=='chainShape'].values[0][1]
                    maxTime = initial_conditions.loc[initial_conditions['Parameter'] == 't_max'].values[0][1]
                    cellradius = initial_conditions.loc[initial_conditions['Parameter'] == 'cellradius'].values[0][1]

                    if not os.path.isfile(filename+'/celldf_with_first_cell_every_nth.csv'):
                        print("No every Nth file present")
                    else:

                        # Check leader overtakes
                        cellpositions_df = pd.read_csv(filename+'/celldf_with_first_cell_every_nth.csv')


                        overal_max_intercell_distance = max_intercell_distances(cellpositions_df, PMZheight, Clength)


                        data = {
                                'leader_k': round(leader_k, 8),
                                'leader_De': round(leader_De, 8),
                                'leader_a': round(leader_autonomousMag, 8),
                                'follower_k': round(follower_k, 8),
                                'follower_De': round(follower_De, 8),
                                'follower_a': round(follower_autonomousMag, 8),
                                'experimentType': experimentType,
                                'overal_max_intercell_distance': overal_max_intercell_distance,
								'middle_zone_height': middle_zone_height,
                                'filename': filename
                                }

                        run_output = pd.DataFrame(data, index=[0])

                        # Add individual simulation output to dataframe
                        result_df = result_df.append(run_output, sort=True)

            except FileNotFoundError:
                print("File not found")
                print(filename)
            except pd.errors.EmptyDataError:
                print("EmptyDataError")
                print(filename)
                pass
            except IndexError:
                print("IndexError")
                print(filename)
            except TypeError:
                print("TypeError")
                print(filename)


result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_1_max_intercell_distances_' + str(ARRAY_INDEX) +'.csv')
