#!/bin/bash

#SBATCH --qos=short
#SBATCH --job-name=core_mult_runs
#SBATCH --array=0-49
#SBATCH --output=core-%A_%a.out
#SBATCH --error=core-%A_%a.err
#SBATCH --account=copan
#SBATCH --workdir=/p/tmp/marcwie/corefinal

python3 $HOME/pycopancore/studies/esd_description_paper_example/submit_single_runs.py
