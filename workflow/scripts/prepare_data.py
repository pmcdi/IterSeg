import argparse
import os
import subprocess

from damply import dirs


def main():
    parser = argparse.ArgumentParser(description="Run nnUNet pipeline on a given dataset.")
    
    # Positional arguments (required by default)
    parser.add_argument("dataset_id", type=str, help="Dataset identifier (<dataset_source>_<dataset_name>)")
    parser.add_argument("dataset_date", type=str, help="Date of dataset collection (YYYY-MM-DD)")

    # Optional args
    parser.add_argument(
        "-m", "--modalities",
        type=str,
        default="CT,RTSTRUCT",
        help="Comma-separated list of modalities (default: CT,RTSTRUCT)"
    )
    parser.add_argument(
        "-ms", "--mask_saving_strategy",
        choices=["label_image", "sparse_mask", "region_mask"],
        default="sparse_mask",
        help="Mask saving strategy (default: sparse_mask)"
    )

    args = parser.parse_args()

    # Build paths
    data_dir = dirs.RAWDATA / args.dataset_id / f"{args.dataset_date}__{args.dataset_id}"
    proc_dir = dirs.PROCDATA / args.dataset_id / f"{args.dataset_date}__{args.dataset_id}"
    config_path = dirs.CONFIG / f"roi_{args.dataset_id}.yaml"

    # Validate paths
    assert data_dir.is_dir(), f"[ERROR] Input data directory not found: {data_dir}"
    assert config_path.exists(), f"[ERROR] ROI YAML config not found: {config_path}"
    proc_dir.mkdir(parents=True, exist_ok=True)

    # Run nnUNet pipeline
    cmd = [
        "imgtools", "-vvv", "nnunet-pipeline",
        data_dir.as_posix(),
        proc_dir.as_posix(),
        "-m", args.modalities,
        "-ryaml", config_path.as_posix(),
        "-ms", args.mask_saving_strategy,
    ]

    print(f"[INFO] Running command:\n{' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] imgtools command failed: {e}")
        return
    
    # Run nnUNet preprocessing
    assert (proc_dir / "nnUNet_raw").exists(), "[ERROR] nnUNet_raw path not found"
    assert (proc_dir / "nnUNet_preprocessed").exists(), "[ERROR] nnUNet_preprocessed path not found"
    assert (proc_dir / "nnUNet_results").exists(), "[ERROR] nnUNet_results path not found"

    env = os.environ.copy()
    env["nnUNet_raw"] = (proc_dir / "nnUNet_raw").as_posix()
    env["nnUNet_preprocessed"] = (proc_dir / "nnUNet_preprocessed").as_posix()
    env["nnUNet_results"] = (proc_dir / "nnUNet_results").as_posix()

    try:
        subprocess.run(
            ["nnUNetv2_plan_and_preprocess", "-d", "1", "--verify_dataset_integrity", "-c", "3d_fullres"],
            env=env,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] nnUNet preprocessing failed: {e}")
        return

if __name__ == "__main__":
    main()
