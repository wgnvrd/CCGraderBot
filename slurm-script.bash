#!/bin/bash
#SBATCH --job-name=Autograder
#SBATCH --output=autograder.out
#SBATCH nodes=1
#SBATCH --time=00:00:40

module load anaconda/3
python testing.py