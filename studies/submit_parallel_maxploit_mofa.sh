#!/bin/bash
#SBATCH --qos=priority
#SBATCH --job-name=full_model_new_thresholds_64_4
#SBATCH --account=copan
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --output=full_model_new_thresholds_64_4%j.out
#SBATCH --error=full_model_new_thresholds_64_4%j.err
#SBATCH --workdir=/p/tmp/maxbecht/results/full_model_new_thresholds_64_4


echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python projects/copan/users/maxbecht/pycopancore/studies/run_parallel_maxploit_mofa.py
