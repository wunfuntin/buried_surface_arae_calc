import pandas as pd

input_file = ('/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/alphafold/'
              'score_files/AF2_run_10_out.sc')
output_file = ('/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/alphafold/'
               'score_files/AF2_run_10_formated.sc')

# Read the file
df = pd.read_csv(input_file, delim_whitespace=True, header=None)

# Drop the first two columns
df.drop([0, 1], axis=1, inplace=True)

# Rename columns for clarity
df.columns = range(df.shape[1])


# Extract the number and reformat the 'description' column
# Drop 'AF2_design_' and append '_run_1'
df[0] = df[0].apply(lambda x: x.split('_')[1] + '_run_10' if '_' in x else x)


# Extract 'x' and reformat the description
# Assuming the 'description' is now in the first column after dropping two columns
df[7] = df[7].apply(lambda x: f"AF2_design_{x.split('_')[1]}_run_10" if '_' in x else x)


# Reorder the DataFrame to make the modified description the first column
cols = df.columns.tolist()
cols = [cols[7]] + cols[1:6]
df = df[cols]

print(df.columns)

df[7] = df[7].str.replace('AF2_design_', '')
# Drop the original description column
# df.drop(df.columns[7], axis=1, inplace=True)
# Write to a new file
df.to_csv(output_file, sep=' ', index=False, header=False)
