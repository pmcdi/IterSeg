#!/usr/bin/env python
#SBATCH --job-name=prepare_data
#SBATCH --mem=64G
#SBATCH -t 2:59:59
#SBATCH -c 24
#SBATCH -N 1
#SBATCH --partition=himem

import sys
import subprocess

from damply import dirs


def main():
    # Check args
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <dataset_id> <dataset_date>")
        sys.exit(1)

    dataset_id = sys.argv[1]
    dataset_date = sys.argv[2]

    # Path to prepare_data.py (assumed in same dir as this script)
    prepare_py = dirs.SCRIPTS / "prepare_data.py"

    # Build command to run inside conda env
    # Use `conda run` to activate environment without sourcing bashrc
    cmd = [
        "conda", "run", "-n", "iterseg",
        "python", str(prepare_py),
        dataset_id, dataset_date
    ]

    print("Running command:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("prepare_data.py finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"prepare_data.py failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
