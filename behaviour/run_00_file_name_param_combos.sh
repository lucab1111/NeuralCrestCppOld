#!/bin/bash
#SBATCH --job-name=NCC_Sim 
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64GB 
#SBATCH --partition=cpu
#SBATCH --time=0-05:00:00
#SBATCH --exclusive
#SBATCH --mail-type=ALL

ml Python/3.7.4-GCCcore-8.3.0;
ml Anaconda2;
source activate pandasTest;

python3 score_00_file_name_param_combos.py ../output;