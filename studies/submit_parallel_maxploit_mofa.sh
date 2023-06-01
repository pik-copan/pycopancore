#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=full_model_groups_0
#SBATCH --account=copan
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --output=full_model_groups_0%j.out
#SBATCH --error=full_model_groups_0%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/results/maxploit3/full_model_groups_0


echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/run_parallel_maxploit_mofa.py
