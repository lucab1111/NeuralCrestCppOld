import os
import pandas as pd
from sys import argv
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

BATCH_PROCESSING_FLAG = 0#argv[1]
ARRAY_INDEX = 1#argv[2]
NUMBER_BUCKETS = 1#argv[3]
OUTPUT_DIRECTORY = '/Users/feldnerd/Documents/GitHub/NeuralCrestCpp/output'#argv[4]

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


result_df = pd.DataFrame(columns = ['PMZcellspeed',
                                    'Followercellspeed',
                                    'Leadercellspeed',
                                    'experimentType',
                                    'leader_autonomousMag',
                                    'leader_De',
                                    'leader_k',
                                    'leader_interactionThreshold',
                                    'follower_autonomousMag',
                                    'follower_De',
                                    'follower_k',
                                    'follower_interactionThreshold',
                                    'PMZheight',
                                    'parameter_key',
                                    'filename'])



def add_speed_column(cellpositions_df):

    speed_df = pd.DataFrame()

    # Remove pmz cells
    cellpositions_df = cellpositions_df.query("cell_type != 0")

    # Only look at every 100th timestep
    cellpositions_df = cellpositions_df.query("everynth != 0")

    cell_list = cellpositions_df.ListName.unique()

    for cell in cell_list:

        cell_data = cellpositions_df.query("ListName == @cell")

        cell_data['previous_y'] = cell_data['Y_microns'].shift(1)
        cell_data['previous_x'] = cell_data['X_microns'].shift(1)

        cell_data['Speed_2D'] = np.sqrt((cell_data['Y_microns'] - cell_data['previous_y'])**2 + ( cell_data['X_microns'] - cell_data['previous_x'])**2 ) * 57


        speed_df = speed_df.append(cell_data)
        
    # Pivot on cell type and condition
    lf_table = pd.pivot_table(speed_df, 
                           values='Speed_2D',
                           columns=['leading_cell_boolean'],
                           aggfunc=np.mean)
    
    return lf_table


# Comment this out to calculate speed for entire set
listdf = pd.read_csv('winning_combo_files.csv',
                    names = ['filename'])
list_array = listdf.filename.values

# Loop through all files and get a table of results
for file_index in range(len(file_list)):
    
    try:

        filename = file_list[file_index]
        print(filename)
        # Get df of initial conditions
        initial_conditions = pd.read_csv(filename+'/initialconditions.txt',header=None,delimiter=r"\s+")
        initial_conditions.columns = ['Parameter','Value']
        #print(initial_conditions)
        
        # Comment this out to calculate speed for entire set
        if filename in list_array:
        
        

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

            cellpositions_df = pd.read_csv(filename+'/celldf_with_first_cell.csv',
                             engine = 'python')

            lf_table = add_speed_column(cellpositions_df)
            cell_types_present = lf_table.columns

            # if 0 in cell_types_present:
            #     PMZcellspeed = lf_table[0].values[0]
            # else:
            #     PMZcellspeed = 'NaN'

            # if 1 in cell_types_present:
            #     Followercellspeed = lf_table[1].values[0]
            # else:
            #     Followercellspeed = 'NaN'

            # if 2 in cell_types_present:
            #     Leadercellspeed = lf_table[2].values[0]
            # else:
            #     Leadercellspeed = 'NaN'

            PMZcellspeed = 'NaN'
            Followercellspeed = lf_table[0].values[0]
            Leadercellspeed = lf_table[1].values[0]

            # Df from dictionary
            data = {'PMZcellspeed': [PMZcellspeed],
                    'Followercellspeed': [Followercellspeed],
                    'Leadercellspeed': [Leadercellspeed],
                    'experimentType': [experimentType],
                   'leader_autonomousMag': [leader_autonomousMag],
                   'leader_De': [leader_De],
                   'leader_interactionThreshold': [leader_interactionThreshold],
                   'follower_autonomousMag': [follower_autonomousMag],
                   'follower_De': [follower_De],
                   'follower_interactionThreshold': [follower_interactionThreshold],
                   'PMZheight': [PMZheight],
                   'leader_k': [leader_k],
                   'follower_k': [follower_k],
                   'parameter_key': [str(leader_autonomousMag)+"_" + \
                                    str(leader_De)+"_"+ \
                                    str(leader_interactionThreshold)+"_"+ \
                                    str(follower_autonomousMag)+"_"+ \
                                    str(follower_De)+"_"+ \
                                    str(leader_k)+"_"+ \
                                    str(follower_k)+"_"+ \
                                    str(PMZheight)+"_"+ \
                                    str(follower_interactionThreshold)],
                   'filename': [filename]}
            single_result_df = pd.DataFrame.from_dict(data)
            print(single_result_df)
            result_df = result_df.append(single_result_df)
            
    except FileNotFoundError:
        print(filename)
        print:("File not found")
        pass
    except KeyError:
        print(filename)
        print:("KeyError")
        pass
    except IndexError:
        print(filename)
        print:("IndexError")
        pass
    except pd.errors.EmptyDataError:
        print(filename)
        print:("pd.errors.EmptyDataError")
        pass
    except TypeError:
        print(filename)
        print:("TypeError")
        pass
    
result_df.reset_index()

result_df.to_csv('speed_results' + str(ARRAY_INDEX) + '.csv')



