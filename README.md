# IterSeg: Iterative Segmentation Framework  

**IterSeg** is an iterative learning framework for medical image segmentation, inspired by the approach used in *TotalSegmentator* [(Wasserthal et al., 2023)](https://doi.org/10.1148/ryai.230024). This framework facilitates semi-automated segmentation by leveraging an initial set of manually labeled cases to train a preliminary model, which is then refined iteratively.  

By integrating `med-imgtools` for preprocessing and `nnUNet` for segmentation, **IterSeg** streamlines the annotation workflow, reducing manual effort while improving segmentation accuracy.  

## Install

First install pixi [here](https://pixi.sh/latest/)

Then run:
```console
pixi install
```
```console
pixi run pip install -e git+https://github.com/bhklab/med-imagetools.git@JoshuaSiraj/update_to_nnUnetv2#egg=med-imagetools
```

## Process  

To run preprocessing, use the following command:  

```console
pixi run preprocess INPUT_DIRECTORY OUTPUT_DIRECTORY --modalities MODALITY_LIST --roi_yaml_path CONFIG_FILE
```