import json

# Load the JSON data from the file
with open('/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/Ryan'
          '/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/run_10_pc/run_10.json', 'r') as file:
    data = json.load(file)

# Iterate through the items and update the specified keys
for key, value in data.items():
    for sub_key in ["PDB_1", "PDB_2", "design_name"]:
        if sub_key in value:
            file_name, file_extension = value[sub_key].split('.')
            value[sub_key] = f"{file_name}_run_10.{file_extension}"

# Write the updated JSON data back to the file
with open('/Users/rwalker/University of Cincinnati/Thompson, Thomas (thompstb) - Tom_Thompson_Lab/Lab Members/Ryan'
          '/RFdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_characterization/run_10_pc/run_10_renamed.json', 'w') as file:
    json.dump(data, file, indent=4)