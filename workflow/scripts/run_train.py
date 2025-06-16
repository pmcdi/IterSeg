#!/usr/bin/env python
#SBATCH --job-name=train_%j
#SBATCH --mem=84G
#SBATCH --gres=gpu:v100:3
#SBATCH -t 2-23:59:59
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --account=radiomics_gpu
#SBATCH --partition=gpu_radiomics
#SBATCH -C "gpu32g"
#SBATCH --mail-type=BEGIN,END,FAIL

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

    # Optional: default values for GPUs and folds
    gpus = [0, 1, 2]
    folds = [0, 1, 2]

    # Path to train.py (assumed to be in same directory as this script)
    train_py = dirs.SCRIPTS / "train.py"

    # Prepare command
    cmd = [
        "conda", "run", "-n", "iterseg",
        "python", str(train_py),
        dataset_id, dataset_date,
        "--gpus", *map(str, gpus),
        "--folds", *map(str, folds),
    ]

    print("Running command:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("✅ train.py finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ train.py failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
