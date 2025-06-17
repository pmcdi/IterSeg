import argparse
import os
import subprocess
from pathlib import Path
from damply import dirs


def run_training_job(gpu: int, fold: int, dataset_id: str, env: dict, pretrained: bool = True) -> subprocess.Popen:

    cmd = [
        "nnUNetv2_train",
        "1",                  
        "3d_fullres",
        str(fold),
    ]

    if pretrained:
        weights_path = (
            dirs.RESULTS / dataset_id / "latest"
            / f"fold_{fold}"
            / "checkpoint_best.pth"
        )
        assert weights_path.exists(), f"[ERROR] Pretrained weights not found: {weights_path}"

        cmd.append("--pretrained_weights")
        cmd.append(weights_path.as_posix())
    else:
        cmd.append("--c")

    gpu_env = env.copy()
    gpu_env["CUDA_VISIBLE_DEVICES"] = str(gpu)

    print(f"[INFO] Launching fold {fold} on GPU {gpu}")
    return subprocess.Popen(cmd, env=gpu_env)


def main():
    parser = argparse.ArgumentParser(description="Train nnUNet folds on multiple GPUs.")
    parser.add_argument("dataset_id", type=str, help="Dataset identifier (e.g., iaslc_data)")
    parser.add_argument("dataset_date", type=str, help="Dataset collection date (e.g., 2024-12-01)")
    parser.add_argument("--pretrained", type=bool, default=True, help="Use pretrained weights")
    parser.add_argument("--gpus", type=int, nargs="+", default=[0, 1, 2, 3, 4], help="List of GPUs to use (e.g., 0 1 2 3)")
    parser.add_argument("--folds", type=int, nargs="+", default=[0, 1, 2, 3, 4], help="List of folds to train")

    args = parser.parse_args()

    # Set up env vars for nnUNet
    proc_dir = dirs.PROCDATA / args.dataset_id / f"{args.dataset_date}__{args.dataset_id}"
    env = os.environ.copy()
    env["nnUNet_raw"] = str(proc_dir / "nnUNet_raw")
    env["nnUNet_preprocessed"] = str(proc_dir / "nnUNet_preprocessed")
    env["nnUNet_results"] = str(proc_dir / "nnUNet_results")

    for key in ["nnUNet_raw", "nnUNet_preprocessed", "nnUNet_results"]:
        assert Path(env[key]).exists(), f"[ERROR] nnUNet env path does not exist: {env[key]}"
        print(f"[INFO] {key} = {env[key]}")

    # Launch training jobs
    processes = []
    for gpu, fold in zip(args.gpus, args.folds):
        proc = run_training_job(gpu, fold, args.dataset_id, env, args.pretrained)
        processes.append(proc)

    # Wait for all to finish
    for proc in processes:
        proc.wait()

    print("[INFO] All training jobs completed.")

    (dirs.RESULTS / args.dataset_id / "latest").symlink_to(
        proc_dir / 
        "nnUNet_results" / 
        f"Dataset001_{args.dataset_date}__{args.dataset_id}" /
        "nnUNetTrainer__nnUNetPlans__3d_fullres"
    )


if __name__ == "__main__":
    main()
