#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=plot_injunctive_timescale
#SBATCH --account=copan
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --output=plot_injunctive_timescale-%j.out
#SBATCH --error=plot_injunctive_timescale-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/plots/injunctive_timescale

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/pt/plot_maxploit_mofa_cluster.py
