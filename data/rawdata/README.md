# Raw Data Directory

## Purpose

This directory stores raw DICOM files. The format of this directory should be as follows:

```bash
rawdata/
└── <dataset_source>_<dataset_name>/ # Every dataset should have its own directory
   └── <year>-<month>-<day>__<dataset_source>_<dataset_name>/ # Every new iteration of the dataset should be saved with prefix of date
```

Example:

```bash
rawdata
└── PM_IASLC
   ├── 2025-03-03__PM_IASLC
   └── 2025-06-05__PM_IASLC
```


