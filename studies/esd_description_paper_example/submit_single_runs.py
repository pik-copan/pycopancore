import os

try:
    TASK = os.environ['SLURM_ARRAY_TASK_ID']
except KeyError:
    print("Not running with SLURM job arrays")
    TASK = 0

HOME = os.path.expanduser("~")
PATH = HOME + "/pycopancore/studies/esd_description_paper_example/"\
        "run_esd_example.py"

for seed in range(50):
    cmd = f"python {PATH} -s {seed} -i {TASK} -p 0.25 --with-social"
    os.system(cmd)
