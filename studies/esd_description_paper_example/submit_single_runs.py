import os

try:
    task = os.environ['SLURM_ARRAY_TASK_ID']
except KeyError:
    print("Not running with SLURM job arrays")
    task = 0

home = os.path.expanduser("~")
path = home + "/pycopancore/studies/esd_description_paper_example/"\
        "run_esd_example.py"

for seed in range(50):
    cmd = f"python {path} -s {seed} -i {task} -p 0.25 --with-social"
    os.system(cmd)
