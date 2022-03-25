import os
import pandas as pd
from sys import argv

#OUTPUT_DIRECTORY = argv[1]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIRECTORY = '../output'

print(OUTPUT_DIRECTORY)

file_list = [file[0] for file in os.walk(OUTPUT_DIRECTORY)]

result_df = pd.DataFrame()

# Find leader final coords
def find_cells_final_coords(cellpositions_df):

    # Find max time
    maxtime = max(cellpositions_df.Time)


    # Get df of last time step
    final_timestep = cellpositions_df.query("Time == @maxtime")


    # Cell list
    cell_list = final_timestep.ListName.values

    # Cell types
    cell_type_list = final_timestep.cell_type.values

    # Leading cell list
    leading_cell_list = final_timestep.leading_cell_boolean.values

    # Get lowest y coord
    lowest_cell_y_coord = final_timestep.Y_microns.values

    # Get x coord of cell with lowest y coord
    corresponding_x_coord = final_timestep.X_microns.values

    return (cell_list, lowest_cell_y_coord, corresponding_x_coord, cell_type_list, leading_cell_list)

i = 0
# Loop through all files and get a table of results
for file_index in range(len(file_list)):

    try:

        filename = file_list[file_index]
        # print(filename)
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


        if follower_k == 0.01 and follower_De == 0.00003 and follower_autonomousMag == 0.000000111111:
            if leader_k == 0.02 and leader_De == 0.00006 and leader_autonomousMag == 0.000003:

                cellpositions_df = pd.read_csv(filename+'/celldf_with_first_cell_every20.csv')

                # returns a list
                cells_final_position = find_cells_final_coords(cellpositions_df)

                for cell in cells_final_position[0]:

                    cell_name = cells_final_position[0][cell]
                    cell_final_y = cells_final_position[1][cell]
                    cell_final_x = cells_final_position[2][cell]
                    cell_type = cells_final_position[3][cell]
                    cell_leading = cells_final_position[4][cell]

                    # Df from dictionary
                    data = {'ListName': [cell_name],
                            'final_y': [cell_final_y],
                            'final_x': [cell_final_x],
                            'cell_type': [cell_type],
                            'leading_cell': [cell_leading],
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
                    #print(single_result_df)
                    result_df = result_df.append(single_result_df)
                    print(i)
                    i = i+1

    except FileNotFoundError:
        print(filename)
        print("File not found")
    except pd.errors.EmptyDataError:
        print("EmptyDataError")
        print(filename)
        pass
    except IndexError:
        print("IndexError")
        print(filename)


result_df.reset_index()

result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_5_targetted_ventral_distance.csv')
