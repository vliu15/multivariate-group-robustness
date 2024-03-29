"""
Batched version of scripts/spurious_matrix.py.

`meta_log_dir` should point to a folder that contains all the log directories
that should be run through scripts/spurious_matrix.py

Sample usage:
python -m scripts.run_spurious_matrix \
    --meta_log_dir logs/spurious_id \
    --json_dir outputs/spurious_eval \
    --mode debug
"""

import argparse
import os

from scripts.job_manager import JobManager


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--meta_log_dir", type=str, required=True, help="Directory of all log directories to create spurious matrix on"
    )
    parser.add_argument(
        "--json_dir",
        type=str,
        required=False,
        default="outputs/spurious_eval",
        help="Path to json directory dumped by this script"
    )
    parser.add_argument(
        "--template", type=str, default="scripts/sbatch_template_rice.sh", required=False, help="SBATCH template file"
    )
    parser.add_argument(
        "--slurm_logs", type=str, default="./slurm_logs", required=False, help="Directory to output slurm logs"
    )
    parser.add_argument("--mode", type=str, choices=["debug", "shell", "sbatch"], default="debug", help="Spawn job mode")
    return parser.parse_args()


def main():
    args = parse_args()
    job_manager = JobManager(mode=args.mode, template=args.template, slurm_logs=args.slurm_logs)

    args = parse_args()
    for log_dir in os.listdir(args.meta_log_dir):
        job_name = f"SPURIOUS_{log_dir}"
        log_file = os.path.join("./slurm_logs", f"{job_name}.log")
        log_dir = os.path.join(args.meta_log_dir, log_dir)
        command = f"python -m scripts.spurious_analysis --log_dir {log_dir} --json_dir {args.json_dir}"
        job_manager.submit(command, job_name=job_name, log_file=log_file)


if __name__ == "__main__":
    main()
