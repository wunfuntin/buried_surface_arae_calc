import pandas as pd

input_json_file = ('/Users/rwalker/Desktop/Big_diffusion_run_final_data_files/combined_json_file.json')
input_csv_file = ('/Users/rwalker/Desktop/Big_diffusion_run_final_data_files/combined_score_file.csv')
output_file = ('/Users/rwalker/Desktop/Big_diffusion_run_final_data_files/combined_data.csv')

# Read the file
json_df = pd.read_json(input_json_file, orient='index')
csv_df = pd.read_csv(input_csv_file, delim_whitespace=True)

json_df_transposed = json_df.transpose()

# Merge csv_df and json_df based on the 'description' column
merged_df = pd.merge(csv_df, json_df, left_on='description', right_index=True)

# Display the first few rows of the merged dataframe
merged_df.head()

merged_df.to_csv(output_file, index=False)