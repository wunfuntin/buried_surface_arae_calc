import json
import os

# List of JSON files to update
files_to_update = ['/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/'
                   'Ryan/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/all_json_files/'
                   'run_10_renamed.json']

# Function to append '_run_1' to all keys
def append_to_keys(data):
    new_data = {}
    for key in data:
        new_data[key + '_run_10'] = data[key]
    return new_data

# Iterate over the files and update them
for file_name in files_to_update:
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)

        # Append '_run_1' to each key
        data = append_to_keys(data)

        # Write the updated data back to the file
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print(f"File not found: {file_name}")