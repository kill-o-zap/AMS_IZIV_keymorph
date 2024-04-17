#!/bin/bash
#
#SBATCH --job-name=run_synthseg # give your job a name
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=120:00:00 # set this time according to your need
#SBATCH --mem=64GB # how much RAM will your notebook consume? 
#SBATCH --gres=gpu:1 # if you need to use a GPU
#SBATCH -p sablab-gpu # specify partition
#SBATCH -o ./job_out/%j-run_synthseg.out
#SBATCH -e ./job_err/%j-run_synthseg.err \ 

# if using conda
source /midtier/sablab/scratch/alw4013/miniconda3/bin/activate synthseg_38
# if using pip
# source ~/myvev/bin/activate

python /home/alw4013/keymorph/gigamed/data_scripts/synthseg.py