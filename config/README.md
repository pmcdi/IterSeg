# ROI YAML Config Files

Each dataset requires a YAML configuration file specifying the ROIs (regions of interest) to extract during preprocessing.

- **Naming convention:** The config file should be named `roi_<dataset_id>.yaml`.
- **Location:** Place the config file in this `config/` directory.

## Example

For a dataset with ID `PM_IASLC`, the config file should be named:

```
roi_PM_IASLC.yaml
```

Example contents:

```yaml
GTV: GTV.*
```

This will match all ROIs with names starting with `GTV`. 

For more information, see the med-imagetools documentation [here](https://bhklab.github.io/med-imagetools)