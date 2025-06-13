import SimpleITK as sitk

def read_dicom_series(
    path: str,
    series_id: list[str] | None = None,
) -> sitk.Image:
    """Read DICOM series as SimpleITK Image.

    Parameters
    ----------
    path
       Path to directory containing the DICOM series.

    series_id, optional
       Specifies the DICOM series to load if multiple series are present in
       the directory. If None and multiple series are present, loads the first
       series found.

    Returns
    -------
    The loaded image.
    """
    reader = sitk.ImageSeriesReader()
    file_names = reader.GetGDCMSeriesFileNames(
        path,
        seriesID=series_id if series_id else "",
    )
    reader.SetFileNames(file_names)

    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()

    return reader.Execute()