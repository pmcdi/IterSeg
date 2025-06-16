import argparse
from datetime import datetime
from pathlib import Path
import subprocess

from damply import dirs


def extract_date(folder_name: str) -> datetime | None:
    try:
        return datetime.strptime(folder_name.split("__")[0], "%Y-%m-%d")
    except Exception:
        return None

def find_latest_date(dataset_id):
    dataset_path = dirs.RAWDATA / dataset_id
    folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    latest_date = None
    for folder in folders:
        date = extract_date(folder.name)
        if date is None:
            continue
        if latest_date is None or date > latest_date:
            latest_date = date
    return latest_date.strftime("%Y-%m-%d")


def submit_sbatch(script: Path, args: list[str], logs_dir: Path, job_tag: str, dependency: str = None) -> str:
    job_name = f"{script.stem}_{job_tag}"  
    output_log = logs_dir / f"{job_name}.out"
    error_log = logs_dir / f"{job_name}.err"

    cmd = [
        "sbatch",
        f"--job-name={job_name}",
        f"--output={output_log}",
        f"--error={error_log}"
    ]

    if dependency:
        cmd.append(f"--dependency=afterok:{dependency}")

    cmd.append(str(script))
    cmd += args

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout.strip()
        print(f"✅ Submitted {script.name}: {output}")
        job_id = output.strip().split()[-1]
        return job_id
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to submit {script.name}")
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise

def main():
    parser = argparse.ArgumentParser(description="Run IterSeg pipeline on a given dataset.")
    parser.add_argument("dataset_id", type=str, help="Dataset identifier (<dataset_source>_<dataset_name>)")

    args = parser.parse_args()

    latest_date = find_latest_date(args.dataset_id)
    print(f"[INFO] Latest date for {args.dataset_id} is {latest_date}")

    if (dirs.PROCDATA / args.dataset_id / f"{latest_date}__{args.dataset_id}").is_dir():
        print(f"[INFO] Data already preprocessed for {args.dataset_id} on {latest_date}")
    else:
        prepare_script = dirs.SCRIPTS / "run_prepare_data.py"
        train_script = dirs.SCRIPTS / "run_train.py"
        script_args = [args.dataset_id, latest_date]

        # Create logs/<latest_date>/ directory
        dated_logs_dir = dirs.LOGS / args.dataset_id / latest_date
        dated_logs_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # e.g., 2025-06-16_14-30-00
        job_tag = f"{args.dataset_id}_{timestamp}"

        prepare_job_id = submit_sbatch(prepare_script, script_args, dated_logs_dir, job_tag=job_tag)
        submit_sbatch(train_script, script_args, dated_logs_dir, job_tag=timestamp, dependency=prepare_job_id)

if __name__ == "__main__":
    main()
