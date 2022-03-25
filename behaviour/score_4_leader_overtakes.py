import pandas as pd
import numpy as np
import sys
import os
from sys import argv
pd.options.mode.chained_assignment = None  # default='warn'

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

def leader_overtakes_count(cell_position_df, PMZheight, Clength, maxTime):

    leader_overtakes = 0

    # Loop over time steps
    list_time_steps = np.sort(cell_position_df.Time.unique())

    if not max(list_time_steps) == maxTime:
        print("Similation ended prematurely")

    else:

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
                #print("Too few timesteps")
                pass

            else:
                #print("Migrating cells present at time " + str(time_step))

                leader_ID = this_time_step_df[this_time_step_df['leading_cell_boolean'] == 1].iloc[0].ListName
                leader_current_rank = this_time_step_df.loc[this_time_step_df['ListName'] == leader_ID, 'rank'].iloc[0]

                previous_timestep_df = migrating_cells_df[migrating_cells_df['Time'] == list_time_steps[time_step - 1]]
                previous_timestep_df['rank'] = previous_timestep_df.Y_microns.rank()

                if not len(previous_timestep_df) > 0:
                    #print("No timesteps before")
                    pass
                else:
                    leader_previous_rank = previous_timestep_df.loc[previous_timestep_df['ListName'] == leader_ID, 'rank'].iloc[0]

                    # Leader rank declined
                    if not leader_current_rank > leader_previous_rank:
                        #print("Leader rank has not declined")
                        pass
                    else:
                        print("Leader rank declined at time " + str(this_time_step))
                        leader_overtakes = leader_overtakes + 1

        return leader_overtakes


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
                        #threshold_time_steps = 4 # How many time steps before considered over take


                        num_leader_overtakes = leader_overtakes_count(cellpositions_df,
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
                                'leader_overtakes': num_leader_overtakes,
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

result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_4_leader_overtake_counts' + str(ARRAY_INDEX) + '.csv')
