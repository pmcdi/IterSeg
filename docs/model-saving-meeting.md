# H4H Model Saving Meeting
Josh, Katy, Jermiah

## [2025-06-11]
### Notes

**Background**

Old Method

- PyTorch lightning setup 
- modules
- train.py called with train.sh

Model Weights

-  .pt = checkpoint path, saved by torch=
- .ckpt and .pt are commonly  used
- can actually be any suffix

Model Definition

- saves layer structure, setup AND weights
- MONAI saves configuration, have their own way of doing it



Now training only nnUnet models

### nnUnet

Requirements

* nnUnet_preprocessed
* nnUNet_raw
    * Training data
    * Can have multiple dataset directories
    * Nifti files
* nnUNet_results


```bash
├── nnUNet_preprocessed
│   ├── Dataset001_FGDLession
│   ├── Dataset002_SARC021
│   ├── Dataset003_RADCURE
│   └── Dataset004_RADCURE_OAR19
├── nnUNet_raw
│   ├── Dataset001_FGDLession
│   ├── Dataset002_SARC021
│   ├── Dataset003_RADCURE
│   ├── Dataset004_RADCURE_OAR19
│   └── scripts
├── nnUNet_results
│   ├── Dataset001_FGDLession
│   ├── Dataset002_SARC021
│   ├── Dataset003_RADCURE
│   └── Dataset004_RADCURE_OAR19
├── nnUnet_weights
│   ├── nnunet_RADCURE_fold_0.pt
│   ├── nnunet_RADCURE_fold_1.pt
│   ├── nnunet_RADCURE_fold_2.pt
│   ├── nnunet_RADCURE_fold_3.pt
│   ├── nnunet_RADCURE_fold_4.pt
│   └── nnunet_RADCURE_model.pt
```

#### Train
```bash
nnUNet_raw/Dataset004_RADCURE_OAR19
├── dataset.json --> configuration of data, what labels are in the data, modalities --> made my med-imagetools
├── imagesTr
├── imagesTs
├── labelsTr
├── labelsTs
```

Other models will follow this setup


#### Preprocessing

* Run nnUnet plan
* validates dataset.json aligns with data
* plans what spacing, window size to use
* saves the plan to preprocessed
* converts segmentation (labels) nifti files to numpys and saves them in preprocessing
* plans for each model available or specified
    * nnUNetPlans_3d_lowres is what Josh uses right now


#### Results

* Saves each fold that was trained
* Contains a log, checkpoint and predicted validation segmentation images
* Maps validation image result to whatever input modality was used
* Checkpoint best and final are saved
    * Josh uses final
* progress.png is validation loss and dice 


### IASLC

* Dataset is distinct between iterations
* Previous iteration data is pre-training data
* Only new data is used for train/validation of each iteration
* Each iteration is fine-tuned

#### Process

1. med-imagetools

2. nnUNet preprocess

3. nnUNet train

### Standards to make

* Naming for nnUNet parent directory
