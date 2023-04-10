#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=plot
#SBATCH --account=copan
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --output=plot-%j.out
#SBATCH --error=plot-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/plots

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/plot_maxploit_mofa_cluster.py
