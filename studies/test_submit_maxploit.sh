#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=test_maxploit
#SBATCH --account=copan
#SBATCH --output=test_maxploit-%j.out
#SBATCH --error=test_maxploit-%j.err
#SBATCH --workdir=/p/tmp/maxbecht/test_jobsubmit

python run_maxploit.py