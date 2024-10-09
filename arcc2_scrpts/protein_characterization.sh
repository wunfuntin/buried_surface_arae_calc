#!/bin/bash

# Set the partition where the job will run
#SBATCH --partition=public
# Set your qos that you want to run under
#SBATCH --qos=proj-411

# Set the number of nodes
#SBATCH --nodes=1
# Set the number of CPUs to use per node
#SBATCH --ntasks-per-node=1
# Set the number of CPUs to use per task
#SBATCH --cpus-per-task=2
# Job memory request
#SBATCH --mem=8

# Set name of job
#SBATCH --job-name=run_2_pc
# Set max wallclock time days-hrs:min:sec
#SBATCH --time=012:00:00

# Set output file name
#SBATCH --output=protein_characterization_run2.out
# Set error file name
#SBATCH --error=protein_characterization_run2.err


module purge
module load anaconda/3.0
module load gcc/12.2.0
module load cuda/11.7.0

conda activate dl_binder_design_again

python /N/lustre/project/proj-411/walker3/rfdiffusion/GDF8_IAP_de_novo_BIG_RUN/protein_mpnn/alphafold/protein_characterization/protein_characterization_v2_cluster.py

