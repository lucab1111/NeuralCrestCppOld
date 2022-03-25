# Python file which goes through a 
# cellpositions file and returns the time point where 
# there first is a cell beyond the bottom of
# the middle zone

import os
import pandas as pd
from sys import argv

BATCH_PROCESSING_FLAG = argv[1]
ARRAY_INDEX = argv[2]
NUMBER_BUCKETS = argv[3]
OUTPUT_DIRECTORY = argv[4]

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


result_df = pd.DataFrame(columns = ['first_time_step_ID',
                                    'experimentType',
                                    'leader_autonomousMag',
                                    'leader_De',
                                    'leader_k',
                                    'leader_interactionThreshold',
                                    'follower_autonomousMag',
                                    'follower_De',
                                    'follower_k',
                                    'follower_interactionThreshold',
                                    'parameter_key',
                                    'filename'])

# load the cellpositions file

# define a function that takes a timestep df and
# determines if one cell is past the mpz
# - takes in timestep df and mpz y coord
# - check if a cell is beyond the mp
# return a one if true, zero otherwise
# pass middle when -PMZheight/2 - Clength - PMZheight - cellradius
# Find cells that have passed the middle

# Check number of cells that have passed border
def cells_out_mp(timestep_cellpositions_df, middle_exit_border):
    
    if len(cellpositions_df.query('y_position < @middle_exit_border').cell_label.unique()) == 1:
    	return 1
    else return 0


# Loop through all files and get a table of results
for file_index in range(len(file_list)):
    
    try:

        filename = file_list[file_index]
        print(filename)
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
        leader_interactionThreshold = initial_conditions.loc[initial_conditions['Parameter']=='leader_interactionThreshold'].values[0][1]
        follower_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='follower_autonomousMag'].values[0][1]
        follower_De = initial_conditions.loc[initial_conditions['Parameter']=='follower_De'].values[0][1]
        follower_interactionThreshold = initial_conditions.loc[initial_conditions['Parameter']=='follower_interactionThreshold'].values[0][1]
        PMZheight = initial_conditions.loc[initial_conditions['Parameter']=='PMZheight'].values[0][1]
        Clength = initial_conditions.loc[initial_conditions['Parameter']=='Clength'].values[0][1]
        cellradius = initial_conditions.loc[initial_conditions['Parameter']=='cellradius'].values[0][1]
        CMwidth = 0.8 
        CEwidth = initial_conditions.loc[initial_conditions['Parameter']=='CEwidth'].values[0][1]
        migratory_zone_border = -PMZheight/2.0 -Clength/10.0
        diamondOffset = (CMwidth-CEwidth)/2.0
        middle_exit_border = -PMZheight/2.0 -Clength -PMZheight -cellradius


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
                    'Nc']

        cellpositions_df = pd.read_csv(filename+'/cellpositions.txt',
                         names = headers,
                         sep = '\s',
                         engine = 'python')

        all_time_steps = cellpositions_df.time.unique()

        first_time_step_flag = False
        first_time_step_ID = -1

        for timestep in all_time_steps:
        	timestep_df = cellpositions_df.query("time == @timestep")

        	if first_time_step_flag == False and cells_out_mp(timestep_df, middle_exit_border) == 1:
        		first_time_step_flag = True 
        		first_time_step_ID = timestep


        number_migrating_cells = cells_out_mp(cellpositions_df, middle_exit_border)

        # Df from dictionary
        data = {'first_time_step_ID': [first_time_step_ID], 
                'experimentType': [experimentType],
               'leader_autonomousMag': [leader_autonomousMag],
               'leader_De': [leader_De],
               'leader_interactionThreshold': [leader_interactionThreshold],
               'follower_autonomousMag': [follower_autonomousMag],
               'follower_De': [follower_De],
               'follower_interactionThreshold': [follower_interactionThreshold],
               'leader_k': [leader_k],
               'follower_k': [follower_k],
               'parameter_key': [str(leader_autonomousMag)+"_" + \
                                str(leader_De)+"_"+ \
                                str(leader_interactionThreshold)+"_"+ \
                                str(follower_autonomousMag)+"_"+ \
                                str(follower_De)+"_"+ \
                                str(leader_k)+"_"+ \
                                str(follower_k)+"_"+ \
                                str(follower_interactionThreshold)],
               'filename': [filename]}
        single_result_df = pd.DataFrame.from_dict(data)
        print(single_result_df)
        result_df = result_df.append(single_result_df)
            
    except FileNotFoundError:
        print(print(filename))
        print:("File not found")
        pass
        
    
result_df.reset_index()

result_df.to_csv('time_step_results_camp_runs_' + str(ARRAY_INDEX) + '.csv')



# go through each timestep - see if there is a middle passer
# if there is - record the timestep and stop looking