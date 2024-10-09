#######-----WORKS-----DO NOT CHANGE------#######

# Import all packages required.
import json
import numpy as np
import os
import pyrosetta
from pyrosetta import rosetta
from pyrosetta.rosetta.core.chemical import VariantType
from pyrosetta.rosetta.core.pose import Pose
from pyrosetta.rosetta.core.select.residue_selector import ChainSelector
from pyrosetta.rosetta.core.scoring import CA_rmsd
import subprocess
import sys
import threading
import time
import xmltodict


# Define the secondary functions utilized.

class StoppableThread(threading.Thread):
    """This is a class that allows for the progress spinner to stop"""

    def __init__(self, target):
        super().__init__(target=target)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def spinner(stop_thread):
    """Creates a spinner while waiting for a process to finish"""
    chars = "/-\|"
    while not stop_thread.stopped():
        for char in chars:
            print(f'\r{char}', end='', flush=True)
            time.sleep(0.1)


def add_directory_to_path(directory):
    """Adds the specified directory to the PATH environment variable."""
    os.environ['PATH'] += os.pathsep + directory


def extract_pdb_from_silent(silent_file, pdb_id, binary_path):
    """
    Extracts a specific pdb file from a .silent file using silent_tools.
    """
    print(f'Extracting silent file: {pdb_id}')
    command = f"{binary_path}/silentextractspecific {silent_file} {pdb_id}"
    print('COMMAND loaded...')

    # Start spinner in a separate thread
    stop_thread = StoppableThread(target=lambda: spinner(stop_thread))
    stop_thread.start()
    print('starting spinner in another thread')
    pdb_file = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    print('Silent file extraction subprocess complete.')
    # Stop spinner
    stop_thread.stop()
    stop_thread.join()

    print(f'\nExtracted file: {pdb_id}')

    return pdb_file


def number_of_pdb_files(silent_file, binary_path):
    """Counts the number of PDBs that are stored in the silent file."""
    command = f"{binary_path}/silentls {silent_file} | wc -l"
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    return int(result.stdout.strip())


def remove_non_protein_residues(pose):
    """
    Remove non-protein residues from the pose such as a phosphate.
    """
    residue_indices_to_remove = []
    for i in range(1, pose.total_residue() + 1):
        if not pose.residue(i).is_protein():
            residue_indices_to_remove.append(i)

    for idx in reversed(residue_indices_to_remove):
        pose.delete_polymer_residue(idx)

    return pose


def extract_chain(pose, chain_id):
    """
    Extract a specific chain from the structure.
    """
    chain_selector = ChainSelector(chain_id)
    chain_map = chain_selector.apply(pose)

    chain_pose = pyrosetta.rosetta.core.pose.Pose()
    for i in range(1, len(chain_map) + 1):
        if chain_map[i]:
            chain_pose.append_residue_by_bond(pose.residue(i))

    return chain_pose


def calculate_sasa(pose):
    """Calculates the surface accessible surface area for a pose."""
    sasa_calc = rosetta.core.scoring.sasa.SasaCalc()
    sasa_calc.calculate(pose)
    return sasa_calc.get_total_sasa()


def run_pisa_shell_script(script_path, i):
    """Initiates a zsh script to run PISA and generate a 'your_file.xml' file."""
    try:
        file_name = f'AF2_design_{i}.pdb'
        command = f'{script_path} {file_name}'
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stderr: {e.stderr}")


def xml_to_json(i):
    """Converts a xml-->json file and writes the json data to json file."""
    # Read the XML file
    with open(f'AF2_design_{i}_out.xml', 'r') as f:
        xml_content = f.read()

    # Convert XML to Python dictionary
    dict_data = xmltodict.parse(xml_content)

    # Convert dictionary to JSON
    json_data_dict = json.dumps(dict_data, indent=4)

    # Write JSON data to a file
    with open(f'AF2_design_{i}_pisa.json', 'w') as j:
        j.write(json_data_dict)


def parse_pisa_data(i):
    """Parses json file created by the 'xml_to_json' function. Then extracts key parameters and collates them into a new json file. Finally, it returns values that can be used as variables in subsequent commands."""
    pisa_res_data = {}

    with open(f'AF2_design_{i}_pisa.json', 'r') as pisa:
        # Step 2: Parse the JSON file
        pisa_data = json.load(pisa)

    int_area = float(pisa_data['pdb_entry']['interface']['int_area'])
    int_solv_en = float(pisa_data['pdb_entry']['interface']['int_solv_en'])
    num_h_bonds = pisa_data['pdb_entry']['interface']['h-bonds']['n_bonds']
    num_salt_bridges = pisa_data['pdb_entry']['interface']['salt-bridges']['n_bonds']

    pisa_int_data = {
        'int_area': int_area.__round__(2),
        'int_solv_en': int_solv_en.__round__(2),
        'num_h_bonds': num_h_bonds,
        'num_salt_bridges': num_salt_bridges,
    }

    pisa_data_entry_number = 0
    for k in range(0, 2):
        for entry in pisa_data['pdb_entry']['interface']['molecule'][k]['residues']['residue']:

            res_solv_en = float((entry['solv_en']))
            if res_solv_en != 0:
                chain_id = pisa_data['pdb_entry']['interface']['molecule'][k]['chain_id']
                chain_number = k + 1
                res_name = entry['name']
                res_num = entry['ser_no']
                asa = float(entry['asa'])
                bsa = float(entry['bsa'])
                bsa_asa_ratio = bsa / asa

                pisa_res_data[pisa_data_entry_number] = {
                    'chain_id': chain_id,
                    'chain_number': chain_number,
                    'res_name': res_name,
                    'res_num': res_num,
                    'asa': asa.__round__(2),
                    'bsa': bsa.__round__(2),
                    'asa_bsa_ratio': bsa_asa_ratio.__round__(2),
                    'solv_en': res_solv_en.__round__(2),
                }

                pisa_data_entry_number += 1

    pisa_int_data['res_data'] = pisa_res_data
    # Convert dictionary to JSON
    json_data_dict = json.dumps(pisa_res_data, indent=4)

    # Write JSON data to a file
    with open(f'AF2_design_{i}_interface.json', 'w') as j:
        j.write(json_data_dict)

    # Return this to use as 'bsa' variable in main() function
    return f'{int_area:.2f}', f'{int_solv_en:.2f}', num_h_bonds, num_salt_bridges


def longest_dimension(pose):
    """Calculates the longest dimension of a molecule in a pose."""
    max_distance = 0
    for i in range(1, pose.total_residue() + 1):
        if pose.pdb_info().chain(i) == 'A':  # Check if the residue is in Chain A
            for j in range(i + 1, pose.total_residue() + 1):
                if pose.pdb_info().chain(j) == 'A':  # Check if the other residue is also in Chain A
                    for atom_i in range(1, pose.residue(i).natoms() + 1):
                        for atom_j in range(1, pose.residue(j).natoms() + 1):
                            distance = pose.residue(i).xyz(atom_i).distance(pose.residue(j).xyz(atom_j))
                            if distance > max_distance:
                                max_distance = distance
    print(f"The longest dimension of Chain A is: {max_distance} Å")
    return max_distance


def extract_and_modify_chain_a(pose):
    """ Extracts chain A and modifies the C-terminus """
    chain_a_pose = Pose()
    for i in range(1, pose.total_residue() + 1):
        if pose.pdb_info().chain(i) == 'A':
            chain_a_pose.append_residue_by_bond(pose.residue(i))

    # Modify the C-terminus of the last residue
    if chain_a_pose.total_residue() > 0:
        last_residue = chain_a_pose.total_residue()
        if not chain_a_pose.residue(last_residue).is_upper_terminus():
            pyrosetta.rosetta.core.pose.add_variant_type_to_pose_residue(
                chain_a_pose, VariantType.CTERM, last_residue)

    return chain_a_pose


def get_chain_pose(pose, chain_id):
    """Extract a specific chain to get a pose."""
    chain_pose = pyrosetta.Pose()
    for i in range(1, pose.total_residue() + 1):
        if pose.pdb_info().chain(i) == chain_id:
            chain_pose.append_residue_by_bond(pose.residue(i))
    return chain_pose


def radius_of_gyration(pose):
    """Calculate the Rg of a pose."""
    # Define a dictionary of atomic weights for common elements
    atomic_weights = {
        "H": 1.008, "HE": 4.002602, "LI": 6.94, "BE": 9.0121831, "B": 10.81, "C": 12.011,
        "N": 14.007, "O": 15.999, "F": 18.998403163, "NE": 20.1797, "NA": 22.98976928,
        "MG": 24.305, "AL": 26.9815385, "SI": 28.085, "P": 30.973761998, "S": 32.06,
        "CL": 35.45, "AR": 39.948, "K": 39.0983, "CA": 40.078, "SC": 44.955908,
    }

    atom_positions = []
    atom_masses = []

    # Extract atom positions and masses
    for i in range(1, pose.total_residue() + 1):
        residue = pose.residue(i)
        for j in range(1, residue.natoms() + 1):
            atom = residue.atom(j)
            element = residue.atom_type(j).element()
            atom_mass = atomic_weights.get(element.upper(), 0)  # Default to 0 if element not found
            atom_positions.append(atom.xyz())
            atom_masses.append(atom_mass)

    # Convert to NumPy arrays
    atom_positions = np.array([np.array([v.x, v.y, v.z]) for v in atom_positions])
    atom_masses = np.array(atom_masses)

    # Calculate center of mass
    mass_sum = np.sum(atom_masses)
    center_of_mass = np.sum(atom_positions.T * atom_masses, axis=1) / mass_sum

    # Calculate the radius of gyration
    distances = np.linalg.norm(atom_positions - center_of_mass, axis=1)
    rg = np.sqrt(np.sum(atom_masses * distances ** 2) / mass_sum)

    return rg


# Main function for running the program.

# Path to the shell script
shell_script_path = '/N/lustre/project/proj-411/walker3/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/alphafold/protein_characterization/run_pisa.sh'

data = {}


def main():
    silent_file1 = "/N/lustre/project/proj-411/walker3/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/alphafold/protein_characterization/RFD_run_1.silent"
    silent_file2 = "/N/lustre/project/proj-411/walker3/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/alphafold/protein_characterization/AF2_run_1.silent"
    binary_path = "/N/lustre/project/proj-411/walker3/RFDiffusion/ProteinMPNN/dl_binder_design/include/silent_tools"

    add_directory_to_path(binary_path)
    pdb_number = number_of_pdb_files(silent_file1, binary_path)

    # Initialize PyRosetta
    pyrosetta.init()

    for i in range(0, pdb_number):
        pdb_id1 = f"design_{i}_dldesign_0_cycle1"
        pdb_id2 = f"design_{i}_dldesign_0_cycle1_af2pred"

        try:
            extract_pdb_from_silent(silent_file1, pdb_id1, binary_path)
            print(f'First pdb extracted: {pdb_id1}')
            pdb1_filename = f'design_{i}_dldesign_0_cycle1.pdb'
            pdb1 = f'RFD_design_{i}.pdb'
            os.rename(pdb1_filename, pdb1)

        except FileNotFoundError:
            print(f'File design_{i}_dldesign_0_cycle1.pdb not found. Skipping to the next file')
            continue

        try:
            extract_pdb_from_silent(silent_file2, pdb_id2, binary_path)
            print(f'Second pdb extracted: {pdb_id2}')
            pdb2_filename = f"design_{i}_dldesign_0_cycle1_af2pred.pdb"
            pdb2 = f'AF2_design_{i}.pdb'
            os.rename(pdb2_filename, pdb2)

        except FileNotFoundError:
            print(f'File design_{i}_dldesign_0_cycle1_af2pred not found.')
        try:
            # Load PDB files
            pose1 = pyrosetta.pose_from_pdb(pdb1)
            pose2 = pyrosetta.pose_from_pdb(pdb2)

            # Remove non-protein residues
            pose1 = remove_non_protein_residues(pose1)
            pose2 = remove_non_protein_residues(pose2)

            # Extract chain A from both structures
            chain_a_pose1 = extract_chain(pose1, 'A')
            chain_a_pose2 = extract_chain(pose2, 'A')

            # Calculate RMSD
            rmsd = CA_rmsd(chain_a_pose1, chain_a_pose2)

            # Generate pose (molecule).
            pose = pyrosetta.pose_from_pdb(pdb2)

            # Calculate SASA for each chain in the unbound state and together
            chain_a_asa = calculate_sasa(pose.split_by_chain(1))
            chain_b_asa = calculate_sasa(pose.split_by_chain(2))
            sasa_complex = calculate_sasa(pose)

            try:
                # Run PISA on current alpha fold file
                run_pisa_shell_script(shell_script_path, i)
                xml_to_json(i)
            except Exception as e:
                print(f'xml to json failed due to {e}')
                if os.path.exists(pdb1):
                    os.remove(pdb1)
                if os.path.exists(pdb2):
                    os.remove(pdb2)
                continue

            try:
                bsa, ddg, num_h_bonds, num_salt_bridges = parse_pisa_data(i)

            except Exception as e:
                print(f'An error occurred: {e}')
                print(f'Skipping design {i} due to file loading error')
                if os.path.exists(pdb1):
                    os.remove(pdb1)
                if os.path.exists(pdb2):
                    os.remove(pdb2)
                continue

            bsa_to_target_asa_ratio = float(bsa) / chain_b_asa
            bsa_to_binder_ratio = float(bsa) / chain_a_asa

            # Calculate the longest dimension of the pose
            longest_dim = longest_dimension(pose)

            # Ratio of interface area to length of the protein.
            int_area_to_length_ratio = float(bsa) / longest_dim

            # Calculate radius of gyration for the entire pose
            rg = radius_of_gyration(pose)

            # Get chain A pose
            chain_a_pose = get_chain_pose(pose, 'A')

            # Get combined chains A and B pose
            chain_ab_pose = get_chain_pose(pose, 'A')
            chain_ab_pose.append_pose_by_jump(get_chain_pose(pose, 'B'), 1)

            # Calculate radius of gyration
            rg_chain_a = radius_of_gyration(chain_a_pose)
            rg_chain_ab = radius_of_gyration(chain_ab_pose)

            new_data_entry = {
                'PDB_1': f'RFD_design_{i}.pdb',
                'PDB_2': f'AF2_design_{i}.pdb',
                'design_name': pdb2,
                'RMSD': f'{rmsd:.2f}',
                'interface_area(ang^2)': bsa,
                'longest_dimension(ang)': f'{longest_dim:.2f}' if longest_dim else None,
                'surf_area_of_complex': f'{sasa_complex:.2f}',
                'int_area_to_len_ratio': f'{int_area_to_length_ratio:.2f}',
                'bsa_to_target_asa_ratio': f'{bsa_to_target_asa_ratio:.2f}',
                'bsa_to_binder_ratio': f'{bsa_to_binder_ratio:.2f}',
                'rg_chain_A': f'{rg_chain_a:.2f}',
                'rg_chain_AB': f'{rg_chain_ab:.2f}',
                'hydrogen_bonds': f'{num_h_bonds}',
                'salt_bridges': f'{num_salt_bridges}',
            }

            # Add the new entry to the data dictionary
            data[i] = new_data_entry
            print('Added data to dictionary.')
            # Clean up extracted files
            os.remove(pdb1)
            os.remove(pdb2)
            os.remove(f'AF2_design_{i}_pisa.json')
            os.remove(f'AF2_design_{i}_out.xml')

        except RuntimeError as e:
            print(f'An error occurred: {e}')
            print(f'Skipping design {i} due to file loading error')
            if os.path.exists(pdb1):
                os.remove(pdb1)
            continue


# Run the full program.

if __name__ == "__main__":
    start_time = time.time()
    main()
    json_data = json.dumps(data, indent=4)
    with open('run_2.json', 'w') as file:
        json.dump(data, file, indent=4)
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = elapsed_time / 36000
    print(f'Script completed in {elapsed_time:.2f} seconds.')
    print(f'Script completed in {hours:.2f} hours.')
    with open('test_script_log.txt', 'a') as log_file:
        # Save the current stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        # Set the new stdout and stderr
        sys.stdout = log_file
        sys.stderr = log_file

        # Reset stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    print("Script execution completed. Check script_log.txt for the log.")