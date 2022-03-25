import pandas as pd
import numpy as np
import sys
import os
from sys import argv
pd.options.mode.chained_assignment = None  # default='warn'

# Must be run from within behaviour
OUTPUT_DIRECTORY = argv[1]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

print(OUTPUT_DIRECTORY)

BATCH_PROCESSING_FLAG = 0
NUMBER_BUCKETS = 45
ARRAY_INDEX = argv[2]

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

def follower_overtakes_count(cell_position_df, PMZheight, Clength, maxTime):


    if not max(cell_position_df.Time) == maxTime:
        print("Simulation ended prematurely")

    else:

        follower_overtakes = 0

        # Only keep every nth timestep
        cell_position_df = cell_position_df.query("everynth == 1")

        # Only consider non-leading cells
        cell_position_df = cell_position_df.query("leading_cell_boolean == 0")

        # Loop over time steps
        list_time_steps = np.sort(cell_position_df.Time.unique())

        # Threshold outside PMZ
        defined_as_migrating = -PMZheight/2 - Clength/10
        migrating_cells_df = cell_position_df.query("Y_microns < @defined_as_migrating")

        # For every time step
        for time_step in range(len(list_time_steps)):

            this_time_step = list_time_steps[time_step]
            last_time_step = list_time_steps[-1]


            # Sub table of all migrating cells, just this time step
            this_time_step_df = migrating_cells_df[migrating_cells_df['Time'] == list_time_steps[time_step]]

            # Rank cells
            rank_series = this_time_step_df.Y_microns.rank()
            this_time_step_df = this_time_step_df.assign(rank=rank_series)

            # Are there cells migrating (outside of PMZ) in this time step?
            if not len(this_time_step_df) > 0:
                pass

            else:
                #print("Migrating cells present at time " + str(time_step))

                if not time_step == 0:

                    #print("current time ")
                    print(list_time_steps[time_step])
                    previous_time_step = list_time_steps[time_step - 1]
                    previous_timestep_df = migrating_cells_df.query("Time == @previous_time_step")
                    #print("Prev ts ")
                    print(previous_time_step)
                    #print("Prev ts df")
                    print(previous_timestep_df)

                    #previous_timestep_df = migrating_cells_df[migrating_cells_df['Time'] == list_time_steps[time_step - 1]]
                    previous_timestep_df['rank'] = previous_timestep_df.Y_microns.rank()

                    for index, row in this_time_step_df.iterrows():

                        current_cell_ID = row['ListName']
                        cell_current_rank = row['rank']

                        if not len(previous_timestep_df) > 0:
                            #print("No timesteps before")
                            pass
                        else:

                            # Check if cell was migrating previously

                            if not current_cell_ID in previous_timestep_df.ListName.values:
                                #print("Cell was not migrating previously")
                                pass

                            else:
                                cell_previous_rank = previous_timestep_df.loc[previous_timestep_df['ListName'] == current_cell_ID, 'rank'].iloc[0]

                                # Cell rank declined
                                if not cell_current_rank > cell_previous_rank:
                                    #print("Cell rank has not declined")
                                    pass
                                else:
                                    #print("Follower rank declined at time " + str(this_time_step))
                                    follower_overtakes = follower_overtakes + 1

        return follower_overtakes


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
                    leader_k = initial_conditions.loc[initial_conditions['Parameter']=='leader_k'].values[0][1]
                    leader_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='leader_autonomousMag'].values[0][1]
                    leader_De = initial_conditions.loc[initial_conditions['Parameter']=='leader_De'].values[0][1]

                    follower_k = initial_conditions.loc[initial_conditions['Parameter']=='follower_k'].values[0][1]
                    follower_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='follower_autonomousMag'].values[0][1]
                    follower_De = initial_conditions.loc[initial_conditions['Parameter']=='follower_De'].values[0][1]

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

                    if not os.path.isfile(filename+'/celldf_with_first_cell_every_nth.csv'):
                        print("No every Nth file present")
                    else:

                        # Check leader overtakes
                        cellpositions_df = pd.read_csv(filename+'/celldf_with_first_cell_every_nth.csv')

                        num_follower_overtakes = follower_overtakes_count(cellpositions_df,
                                                                      PMZheight,
                                                                      Clength,
                                                                      maxTime)


                        data = {
                                'leader_k': round(leader_k, 8),
                                'leader_De': round(leader_De, 8),
                                'leader_a': round(leader_autonomousMag, 8),
                                'follower_k': round(follower_k, 8),
                                'follower_De': round(follower_De, 8),
                                'follower_a': round(follower_autonomousMag, 8),
                                'experimentType': experimentType,
                                'follower_overtakes_count': num_follower_overtakes,
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
            except IndexError:
                print("IndexError")
                print(filename)
            except TypeError:
                print("TypeError")
                print(filename)
            except KeyError:
                print("KeyError")
                print(filename)

result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_2_follower_overtake_counts_' + str(ARRAY_INDEX) + '.csv')
