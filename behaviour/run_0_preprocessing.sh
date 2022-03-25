#!/bin/bash
#SBATCH --job-name=NCC_Sim
#SBATCH --ntasks=1
#SBATCH --mail-user=dylan.feldner-busztin@crick.ac.uk
#SBATCH --cpus-per-task=4
#SBATCH --mem=64GB
#SBATCH --partition=cpu
#SBATCH --time=0-24:00:00
#SBATCH --exclusive
#SBATCH --mail-type=ALL
#SBATCH --array=1-45

ml Python/3.7.4-GCCcore-8.3.0;
ml Anaconda2;
source activate pandasTest;

python3 score_0_preprocessing.py $SLURM_ARRAY_TASK_ID;
