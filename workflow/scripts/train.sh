#!/bin/bash
#SBATCH --job-name=train
#SBATCH --mem=164G
#SBATCH --gres=gpu:v100:5
#SBATCH -t 2-23:59:59
#SBATCH -c 32
#SBATCH -N 1
#SBATCH --account=radiomics_gpu
#SBATCH --partition=gpu_radiomics
#SBATCH -C "gpu32g"
#SBATCH --mail-type=BEGIN,END,FAIL

source ~/.bashrc
conda activate iterseg

set -e

# Ensure at least two positional arguments are given
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <dataset_id> <dataset_date> 
  exit 1
fi

# Positional args
DATASET_ID="$1"
DATASET_DATE="$2"

python3 ./train.py "$DATASET_ID" "$DATASET_DATE" 
