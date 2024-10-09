import json

# List of JSON files to merge
files_to_merge = ['/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_1_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_2_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_3_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_4_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_5_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_6_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_7_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_8_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_9_renamed.json',
                  '/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_10_renamed.json']

# Initialize an empty dictionary to store the merged content
merged_data = {}

# Iterate over the files and merge them
for file_name in files_to_merge:
    with open(file_name, 'r') as file:
        data = json.load(file)
        merged_data.update(data)  # This assumes the keys in each file are unique

# Write the merged data to a new file
with open('/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/'
          'Lab Members/Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
          'merged_file.json', 'w') as file:
    json.dump(merged_data, file, indent=4)