#!/bin/bash
#SBATCH --qos=medium
#SBATCH --job-name=maxploit_mofa_run
#SBATCH --account=copan
#SBATCH --output=maxploit_run-%j.out
#SBATCH --error=maxploit_run-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/pycopancore/studies

python run_maxploit_mofa.py