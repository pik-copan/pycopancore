#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=harvest_final
#SBATCH --account=copan
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --output=harvest_final-%j.out
#SBATCH --error=harvest_final-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/results/maxploit2/harvest_final

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/run_parallel_maxploit_mofa.py
