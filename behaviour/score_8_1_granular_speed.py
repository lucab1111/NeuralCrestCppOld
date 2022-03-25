import os
import pandas as pd
from sys import argv
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

BATCH_PROCESSING_FLAG = 0#argv[1]
ARRAY_INDEX = 1#argv[2]
NUMBER_BUCKETS = 1#argv[3]
OUTPUT_DIRECTORY = '../small_output'#argv[4]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

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



def add_speed_and_filename_column(cellpositions_df, filename):

    speed_df = pd.DataFrame()

    # Remove pmz cells
    cellpositions_df = cellpositions_df.query("cell_type != 0")

    # Only look at every nth timestep
    cellpositions_df = cellpositions_df.query("everynth != 0")

    cell_list = cellpositions_df.ListName.unique()

    for cell in cell_list:

        cell_data = cellpositions_df.query("ListName == @cell")

        cell_data['previous_y'] = cell_data['Y_microns'].shift(1)
        cell_data['previous_x'] = cell_data['X_microns'].shift(1)

        cell_data['Speed_2D'] = np.sqrt((cell_data['Y_microns'] - cell_data['previous_y'])**2 + ( cell_data['X_microns'] - cell_data['previous_x'])**2 ) * 57

        cell_data['filename'] = filename

        speed_df = speed_df.append(cell_data)
    
    return speed_df


# Loop through all files and get a table of results
for file_index in range(len(file_list)):
    
    filename = file_list[file_index]
    print(filename)

    try:

        # Get df of initial conditions
        initial_conditions = pd.read_csv(filename+'/initialconditions.txt',header=None,delimiter=r"\s+")
        initial_conditions.columns = ['Parameter','Value']
        #print(initial_conditions)

        # Extract relevant variables
        leader_k = initial_conditions.loc[initial_conditions['Parameter']=='leader_k'].values[0][1]
        follower_k = initial_conditions.loc[initial_conditions['Parameter']=='follower_k'].values[0][1]
        experimentType = initial_conditions.loc[initial_conditions['Parameter']=='experimentType'].values[0][1]
        leader_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='leader_autonomousMag'].values[0][1]
        leader_De = initial_conditions.loc[initial_conditions['Parameter']=='leader_De'].values[0][1]
        follower_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='follower_autonomousMag'].values[0][1]
        follower_De = initial_conditions.loc[initial_conditions['Parameter']=='follower_De'].values[0][1]

        if follower_k == 0.01 and follower_De == 0.00003 and follower_autonomousMag == 0.000000111111:
            if leader_k == 0.02 and leader_De == 0.00006 and leader_autonomousMag == 0.000003:

        # if True:
        #     if True:

                # Check how many cells migrated
                headers = ['time',
                            'y_position',
                            'x_position',
                            'v_auto_0',
                            'v_auto_1',
                            'v_bound_0',
                            'v_bound_1',
                            'cellradius',
                            'cell_label',
                            'cell_type',
                            'experiment_type',
                            'Nc',
                            'first_cell_out',
                            'leading_cell_boolean']

                cellpositions_df = pd.read_csv(filename+'/celldf_with_first_cell_every20.csv',
                                 engine = 'python')

                run_result = add_speed_and_filename_column(cellpositions_df, filename)

                result_df = result_df.append(run_result)


    except FileNotFoundError:
        print("File not found")
        print(filename)
        pass
    except IndexError:
        print("IndexError")
        print(filename)
        pass
    except pd.errors.EmptyDataError:
        print("pandas.errors.EmptyDataError")
        print(filename)
        pass

    
result_df.reset_index()

result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_8_1_granular_speed.csv')



