# IterSeg: Iterative Segmentation Framework  

**IterSeg** is an iterative learning framework for medical image segmentation, inspired by the approach used in *TotalSegmentator* [(Wasserthal et al., 2023)](https://doi.org/10.1148/ryai.230024). This framework facilitates semi-automated segmentation by leveraging an initial set of manually labeled cases to train a preliminary model, which is then refined iteratively.  

By integrating [`med-imagetools`](https://github.com/bhklab/med-imagetools) for preprocessing and [`nnUNet`](https://github.com/MIC-DKFZ/nnUNet) for segmentation, **IterSeg** streamlines the annotation workflow, reducing manual effort while improving segmentation accuracy.  

## Install

```console
conda env create --name iterseg --file=environment.yml
conda activate iterseg
```

```console
pip install -e git+https://github.com/bhklab/med-imagetools.git@JoshuaSiraj/update_to_nnUnetv2#egg=med-imagetools
```

## Process  

To run preprocessing, use the following command:  

```console
autopipeline \
  [INPUT_DIRECTORY] \
  [OUTPUT_DIRECTORY] \
  --modalities [MODALITIES] \ # Default usage would be CT,RTSTRUCT
  --nnunet \
  --roi_yaml_path [CONFIG_PATH] \ # Example can be found in configs/roi_yaml_example.yaml
  --read_yaml_label_names
```

## Train

You can find the scripts to plan and train an nnUNet model in the output directory provided by med-imagetools.

## Prediction

The prediction module can be found in `src/predict_nnunet.py`.
