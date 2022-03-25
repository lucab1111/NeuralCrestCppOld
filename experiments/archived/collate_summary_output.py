import pandas as pd
import os
import numpy as np

summary_output_df = pd.DataFrame()

SUMMARY_OUTPUT_DIR = 'summary_output'

file_list = [file for file in os.walk(SUMMARY_OUTPUT_DIR)]
file_list = np.asarray(file_list)[0,2]

for file in file_list:
    summary_output_df = summary_output_df.append(pd.read_csv(SUMMARY_OUTPUT_DIR + os.sep + file))

summary_output_df.to_csv('all_sims_output.csv')
