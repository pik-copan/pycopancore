#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=plot_threshold
#SBATCH --account=copan
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --output=plot_threshold-%j.out
#SBATCH --error=plot_threshold-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/plots/descriptive_threshold_final

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/pt/plot_maxploit_mofa_cluster.py
