import os
import pandas as pd
from sys import argv
import math
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

# BATCH_PROCESSING_FLAG = argv[1]
# ARRAY_INDEX = argv[2]
# NUMBER_BUCKETS = argv[3]
#OUTPUT_DIRECTORY = argv[1]

BATCH_PROCESSING_FLAG = 0#argv[1]
ARRAY_INDEX = 1#argv[2]
NUMBER_BUCKETS = 1#argv[3]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIRECTORY = argv[1]

print("Directionality")

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
    print(file_list)

result_df = pd.DataFrame()


def adjacent_over_hypotenuse_ratio(startx, starty, newx, newy):
    Y_change = starty - newy
    Dist2D = math.sqrt((startx - newx) ** 2 + (starty - newy) ** 2)

    if Dist2D != 0:
        adjacent_over_hypotenuse = Y_change / Dist2D
    else:
        adjacent_over_hypotenuse = ''

    return adjacent_over_hypotenuse


def calculate_directionality(cellpositions_df, filename):

    directionality_df = pd.DataFrame()

    # Remove pmz cells
    cellpositions_df = cellpositions_df.query("cell_type != 0")

    # Only look at every 100th timestep
    cellpositions_df = cellpositions_df.query("everynth != 0")

    cell_list = cellpositions_df.ListName.unique()

    for cell in cell_list:

        cell_data = cellpositions_df.query("ListName == @cell")

        # Check that cell got at least as far as the midpoint
        inclusion_start = -0.26 #-1 -0.13
        furthest_point = min(cell_data.Y_microns.values)

        if furthest_point < inclusion_start:

            cell_data['previous_y'] = cell_data['Y_microns'].shift(1)
            cell_data['previous_x'] = cell_data['X_microns'].shift(1)

            cosangle_list = []
            for index, row in cell_data.iterrows():

                cosa = adjacent_over_hypotenuse_ratio(row['previous_x'],
                                                      row['previous_y'],
                                                      row['X_microns'],
                                                      row['Y_microns'])

                cosangle_list.append(cosa)

            cell_data['Cosangle'] = cosangle_list

            cell_data['filename'] = filename


            directionality_df = directionality_df.append(cell_data)

    return directionality_df


# Loop through all files and get a table of results
for file_index in range(len(file_list)):


    filename = file_list[file_index]
    print(filename)

    if filename != OUTPUT_DIRECTORY:

        if os.path.isfile(filename+'/initialconditions.txt'):

            # Get df of initial conditions
            initial_conditions = pd.read_csv(filename+'/initialconditions.txt',header=None,delimiter=r"\s+")
            initial_conditions.columns = ['Parameter','Value']

            if not len(initial_conditions) == 28:
                    print("Initial conditions incomplete")

            else:

                # Extract relevant variables
                leader_k = initial_conditions.loc[initial_conditions['Parameter']=='leader_k'].values[0][1]
                follower_k = initial_conditions.loc[initial_conditions['Parameter']=='follower_k'].values[0][1]
                experimentType = initial_conditions.loc[initial_conditions['Parameter']=='experimentType'].values[0][1]
                leader_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='leader_autonomousMag'].values[0][1]
                leader_De = initial_conditions.loc[initial_conditions['Parameter']=='leader_De'].values[0][1]
                leader_interactionThreshold = initial_conditions.loc[initial_conditions['Parameter']=='leader_interactionThreshold'].values[0][1]
                follower_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='follower_autonomousMag'].values[0][1]
                follower_De = initial_conditions.loc[initial_conditions['Parameter']=='follower_De'].values[0][1]
                follower_interactionThreshold = initial_conditions.loc[initial_conditions['Parameter']=='follower_interactionThreshold'].values[0][1]
                PMZheight = initial_conditions.loc[initial_conditions['Parameter']=='PMZheight'].values[0][1]
                Clength = initial_conditions.loc[initial_conditions['Parameter']=='Clength'].values[0][1]
                CMwidth = 0.8
                CEwidth = initial_conditions.loc[initial_conditions['Parameter']=='CEwidth'].values[0][1]
                migratory_zone_border = -PMZheight/2.0 -Clength/10.0
                diamondOffset = (CMwidth-CEwidth)/2.0
                middle_exit_border = -PMZheight/2.0 -Clength -PMZheight
                middle_zone_height = initial_conditions.loc[initial_conditions['Parameter']=='middle_zone_height'].values[0][1]


                if not os.path.isfile(filename+'/celldf_with_first_cell_every20.csv'):
                    print("No every Nth file present")

                else:

                    cellpositions_df = pd.read_csv(filename+'/celldf_with_first_cell_every20.csv')

                    single_result_df = calculate_directionality(cellpositions_df, filename)

                    # Only add if there is a value for each
                    result_df = result_df.append(single_result_df)


result_df.reset_index()

result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_7_directionality.csv')
