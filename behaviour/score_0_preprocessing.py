import os
import pandas as pd
import numpy as np
from sys import argv

"""

Creates csv files which have kept only every 20th timestep to align better with in vivo timings.

"""


# Path to executable
PRESENT_DIR = os.path.dirname(os.path.realpath(__file__)).replace('behaviour','')
#PRESENT_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = PRESENT_DIR + 'output'
BATCH_PROCESSING_FLAG = 0
NUMBER_BUCKETS = 45
ARRAY_INDEX = argv[1]

print(OUTPUT_DIR)

file_list = [file[0] for file in os.walk(OUTPUT_DIR)]

# If BATCH_PROCESSING_FLAG is 1 then split the data up for parallel processing
if int(BATCH_PROCESSING_FLAG) == 1:
    # Focus on subsection of file_list
    number_of_files = len(file_list)
    number_of_buckets = int(NUMBER_BUCKETS)
    approx_files_per_bucket = int(number_of_files / number_of_buckets)
    lower_bound = int(ARRAY_INDEX) * approx_files_per_bucket
    upper_bound = lower_bound + approx_files_per_bucket
    file_list = file_list[lower_bound:upper_bound]

for file_index in range(len(file_list)):

    file_directory = file_list[file_index]
    print(file_directory)

    check_if_output = file_directory[-6:]

    try:

        if check_if_output != 'output':

            if os.path.isfile(file_directory + os.sep + 'celldf_with_first_cell.csv'):
                print("File exists")
            else:

                # Build initialConditions dataframe
                initialConditions_DF            = pd.read_csv(file_directory + os.sep + 'initialconditions.txt', header=None, delimiter=r"\s+")
                initialConditions_DF.columns    = ['Variable', 'Value']

                # Create dictionary for condition items
                initialConditions_Dict          = {}
                for index, row in initialConditions_DF.iterrows():
                    initialConditions_Dict[row['Variable']] = row['Value']

                # Get NB parameters
                param_PMZh                      = initialConditions_Dict.get('PMZheight')
                param_CElength                  = initialConditions_Dict.get('Clength')


                # Read a csv
                cell_position_df = pd.read_csv(file_directory + os.sep + 'cellpositions.txt',
                                               sep=' ',
                                               header = None)

                cell_position_df.columns = ['Time',
                                            'Y_microns',
                                            'X_microns',
                                            'v_auto_0',
                                            'v_auto_1',
                                            'v_bound_0',
                                            'v_bound_1',
                                            'cellradius',
                                            'ListName',
                                            'cell_type',
                                            'notch',
                                            'dll4',
                                            'experiment_type',
                                            'Nc']

                # Flag
                migration_not_started = 0

                # Obtain timestep list
                timestep_list = cell_position_df.Time.unique()

                # Loop over time steps
                for timestep in timestep_list:
                    #print(timestep)

                    # Query a table for each time step
                    timestep_df = cell_position_df.query("Time == @timestep")
                    # print(timestep_df)

                    # Check the lowest cell in that time step
                    lowest_y_value = timestep_df.Y_microns.min()
                    #print(timestep_df.Y_microns.min())

                    # If its lower than (-params.PMZheight/2.0-params.Clength/5.0)
                    if lowest_y_value < (-param_PMZh/2.0-param_CElength/5.0) and migration_not_started == 0:
                        # It is the first cell out of the PMZ

                        # Check that cell's ID
                        id_of_cell_first_out = timestep_df.loc[timestep_df['Y_microns'] == lowest_y_value, 'ListName'].iloc[0]
                        #print(id_of_cell_first_out)

                        migration_not_started = 1


                cell_position_df['first_cell_out'] = id_of_cell_first_out

                cell_position_df['leading_cell_boolean'] = cell_position_df['ListName'] == id_of_cell_first_out
                cell_position_df['leading_cell_boolean'] = cell_position_df['leading_cell_boolean'].astype(int)
                cell_position_df['Time'] = cell_position_df['Time'].astype(int)

                cell_position_df['everynth'] = (np.mod(cell_position_df['Time'],20) == 0).astype(int)


                cell_position_df.to_csv(file_directory + '/celldf_with_first_cell_every_nth.csv')

    except FileNotFoundError:
        print(file_directory)
        print("File not found")
        pass
    except IndexError:
        print("IndexError")
        print(file_directory)
        pass
    except pd.errors.EmptyDataError:
        print("pandas.errors.EmptyDataError")
        print(file_directory)
        pass
    except TypeError:
        print("TypeError")
        print(file_directory)
        pass
