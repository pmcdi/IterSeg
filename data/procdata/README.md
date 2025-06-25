# Processed Data Directory

This directory stores the processed DICOM files in nnUNet dataset format(saved in .nii.gz format). This is the output directory of the `imgtools nnunet-pipeline` command.

For more information, see the med-imagetools documentation in the nnUNet option [here](https://bhklab.github.io/med-imagetools/)
And the nnUNet documentation [here](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_format.md)

Example Directory Structure:

```bash
├── procdata
│   └── PM_IASLC
│       ├── 2025-03-03__PM_IASLC
│       │   ├── nnUNet_preprocessed
│       │   ├── nnUNet_raw
│       │   └── nnUNet_results
│       └── 2025-06-05__PM_IASLC
│           ├── nnUNet_preprocessed
│           ├── nnUNet_raw
│           └── nnUNet_results
