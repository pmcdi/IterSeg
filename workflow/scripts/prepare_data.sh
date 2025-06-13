#!/bin/sh
#SBATCH --job-name=prepare_data
#SBATCH --mem=64G
#SBATCH -t 2:59:59
#SBATCH -c 24
#SBATCH -N 1
#SBATCH --partition=himem

set -e  # Exit immediately if a command fails

# Ensure at least two positional arguments are given
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <dataset_id> <dataset_date> 
  exit 1
fi

# Positional args
DATASET_ID="$1"
DATASET_DATE="$2"

python3 ./prepare_data.py "$DATASET_ID" "$DATASET_DATE" 
