#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=new_measures_test
#SBATCH --account=copan
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --output=new_measures_test-%j.out
#SBATCH --error=new_measures_test-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/results/maxploit/new_measures_test

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/run_parallel_maxploit_mofa.py
