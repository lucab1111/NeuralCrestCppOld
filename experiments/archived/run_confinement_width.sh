#!/bin/bash
#SBATCH --job-name=NCC_Sim 
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=20GB 
#SBATCH --partition=cpu
#SBATCH --time=0-05:00:00
#SBATCH --array=0-50
#SBATCH --exclusive
#SBATCH --mail-type=ALL

ml Python/3.7.4-GCCcore-8.3.0;
ml Anaconda2;
source activate pandas;

python3 confinement_width.py;