import os
import pandas as pd
from sys import argv

OUTPUT_DIRECTORY = argv[1]

print(OUTPUT_DIRECTORY)

file_list = [file[0] for file in os.walk(OUTPUT_DIRECTORY)]


result_df = pd.DataFrame(columns = ['lowest_y',
                                    'corresponding_x',
                                    'experimentType',
                                    'leader_autonomousMag',
                                    'leader_De',
                                    'leader_k',
                                    'leader_interactionThreshold',
                                    'follower_autonomousMag',
                                    'follower_De',
                                    'follower_k',
                                    'follower_interactionThreshold',
                                    'leader_gradientSensitivity',
                                    'follower_gradientSensitivity',
                                    'PMZheight',
                                    'middle_zone_height',
                                    'Nc',
                                    'CEwidth',
                                    'parameter_key',
                                    'filename'])

# Find leader final coords
def find_leader_final_coords(cellpositions_df):

    # Find max time
    maxtime = max(cellpositions_df.time)

    # Get df of last time step
    final_timestep = cellpositions_df.query("time == @maxtime")

    # Get lowest y coord
    lowest_cell_y_coord = min(final_timestep.y_position)

    # Get x coord of cell with lowest y coord
    corresponding_x_coord = final_timestep.loc[final_timestep['y_position'] == lowest_cell_y_coord].iloc[0].x_position

    return (lowest_cell_y_coord, corresponding_x_coord)


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
        PMZwidth = initial_conditions.loc[initial_conditions['Parameter']=='PMZwidth'].values[0][1]
        Clength = initial_conditions.loc[initial_conditions['Parameter']=='Clength'].values[0][1]
        CMwidth = 0.8 
        CEwidth = initial_conditions.loc[initial_conditions['Parameter']=='CEwidth'].values[0][1]
        migratory_zone_border = -PMZheight/2.0 -Clength/10.0
        diamondOffset = (CMwidth-CEwidth)/2.0
        middle_exit_border = -PMZheight/2.0 -Clength -PMZheight
        Ncells = initial_conditions.loc[initial_conditions['Parameter']=='Nc'].values[0][1]
        middle_zone_height = initial_conditions.loc[initial_conditions['Parameter']=='middle_zone_height'].values[0][1]
        lgrad = initial_conditions.loc[initial_conditions['Parameter']=='leader_gradientSensitivity'].values[0][1]
        fgrad = initial_conditions.loc[initial_conditions['Parameter']=='follower_gradientSensitivity'].values[0][1]
        chainShape = initial_conditions.loc[initial_conditions['Parameter']=='chainShape'].values[0][1]


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

        #number_migrating_cells = cells_out_mp(cellpositions_df, middle_exit_border)
        leader_final_position = find_leader_final_coords(cellpositions_df, )

        # Df from dictionary
        data = {'lowest_y': [leader_final_position[0]],
                'corresponding_x': [leader_final_position[1]],
                'experimentType': [experimentType],
               'leader_autonomousMag': [leader_autonomousMag],
               'leader_De': [leader_De],
               'leader_interactionThreshold': [leader_interactionThreshold],
               'follower_autonomousMag': [follower_autonomousMag],
               'follower_De': [follower_De],
               'follower_interactionThreshold': [follower_interactionThreshold],
               'PMZheight': [PMZheight],
               'CEwidth': [CEwidth],
               'middle_zone_height': [middle_zone_height],
               'Nc': [Ncells],
               'leader_k': [leader_k],
               'follower_k': [follower_k],
               'leader_gradientSensitivity': [lgrad],
               'follower_gradientSensitivity': [fgrad],
               'chainShape': [chainShape],
               'parameter_key': [str(leader_autonomousMag)+"_" + \
                                str(leader_De)+"_"+ \
                                str(leader_interactionThreshold)+"_"+ \
                                str(follower_autonomousMag)+"_"+ \
                                str(follower_De)+"_"+ \
                                str(leader_k)+"_"+ \
                                str(follower_k)+"_"+ \
                                str(middle_zone_height) +"_"+ \
                                str(CEwidth) +"_"+ \
                                str(Ncells) +"_"+ \
                                str(PMZheight)+"_"+ \
                                str(follower_interactionThreshold)+"_"+ \
                                str(fgrad) +"_"+ \
                                str(lgrad)],
               'filename': [filename]}
        single_result_df = pd.DataFrame.from_dict(data)
        print(single_result_df)
        result_df = result_df.append(single_result_df)
            
    except FileNotFoundError:
        print(print(filename))
        print:("File not found")
    except pd.errors.EmptyDataError:
        pass
        
    
result_df.reset_index()

result_df.to_csv('final_position_results' + '.csv')



