import argparse
from datetime import datetime
import subprocess

from damply import dirs


def extract_date(folder_name: str) -> datetime | None:
    try:
        return datetime.strptime(folder_name.split("__")[0], "%Y-%m-%d")
    except Exception:
        return None

def find_latest_date(dataset_id):
    dataset_path = dirs.RAWDATA / dataset_id
    folders = [f for f in dataset_path.listdir() if f.isdir()]
    latest_date = None
    for folder in folders:
        date = extract_date(folder.name)
        if date is None:
            continue
        if latest_date is None or date > latest_date:
            latest_date = date
    return latest_date.strftime("%Y-%m-%d")
    

def main():
    parser = argparse.ArgumentParser(description="Run IterSeg pipeline on a given dataset.")
    parser.add_argument("dataset_id", type=str, help="Dataset identifier (<dataset_source>_<dataset_name>)")

    args = parser.parse_args()

    latest_date = find_latest_date(args.dataset_id)
    
    if dirs.PROCDATA / args.dataset_id / f"{latest_date}__{args.dataset_id}".is_dir():
        print(f"[INFO] Data already preprocessed for {args.dataset_id} on {latest_date}")
    else:
        subprocess.run(["./prepare_data.sh", args.dataset_id, latest_date])
        subprocess.run(["./train.sh", args.dataset_id, latest_date])


