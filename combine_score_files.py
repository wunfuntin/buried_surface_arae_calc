import pandas as pd

# List of file names to combine
file_names = ['/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_1_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_2_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_3_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_4_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_5_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_6_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_7_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_8_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_9_formated.sc',
              '/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/AF2_run_10_formated.sc'
              ]

# Read each file and store in a list
dataframes = [pd.read_csv(file) for file in file_names]

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a new file
combined_df.to_csv('/Users/rwalker/Desktop/RFDiffusion/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/'
              'alphafold/score_files/combined_file.csv', index=False)
