import json
from typing import Tuple, Dict
from pathlib import Path

import numpy as np
import SimpleITK as sitk

from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
from nnunetv2.imageio.simpleitk_reader_writer import SimpleITKIO

from loaders import read_dicom_series

class nnUNetPredictorWrapper:
    """
    A wrapper class for nnUNetPredictor to facilitate prediction from a trained nnUNet model.

    Args:
        model_training_output_dir (str): Directory where the trained model is stored.
        folds (Tuple[int] | None, optional): Specific folds to use for prediction. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the nnUNetPredictor.

    Attributes:
        predictor (nnUNetPredictor): An instance of nnUNetPredictor initialized with the trained model.
    """
    def __init__(
            self, 
            model_training_output_dir: str, 
            folds: Tuple[int] | None = None, 
            **kwargs
        ):
        self.model_training_output_dir = Path(model_training_output_dir)
        with open(self.model_training_output_dir / 'dataset.json') as f:
            self.dataset_info = json.load(f)

        self.predictor = nnUNetPredictor(
            **kwargs
        )
        self.predictor.initialize_from_trained_model_folder(
                model_training_output_dir,
                checkpoint_name='checkpoint_best.pth',
                use_folds=folds
        )

    def _format_output(self, img: sitk.Image, prediction: np.ndarray) -> Dict[str, sitk.Image]:
        labels = self.dataset_info['labels']
        data = {}

        for label, idx in labels.items():
            if idx == 0:
                continue

            label_image = sitk.GetImageFromArray(np.where(prediction == idx, prediction, 0))
            label_image.CopyInformation(img)

            data[label] = label_image

        return data
    
    def predict_from_single_image(self, image_path: str) -> Dict[str, sitk.Image]:
        """
        Predicts segmentation masks from a single image.

        Args:
            image_path (str): The file path to the input image.

        Returns:
            Dict[str, sitk.Image]: A dictionary where keys are label names and values are the corresponding 
                                   SimpleITK images representing the segmentation masks.
        """
        img, metadata = SimpleITKIO().read_images([image_path])
        prediction = self.predictor.predict_single_npy_array(img, metadata, None, None, False)

        return self._format_output(sitk.ReadImage(image_path), prediction)

    def predict_single_dicom(self, image_path: str) -> Dict[str, sitk.Image]:
        """
        Predicts segmentation masks from a single dicom.

        Args:
            image_path (str): The file path to the input dicom.

        Returns:
            Dict[str, sitk.Image]: A dictionary where keys are label names and values are the corresponding 
                                   SimpleITK images representing the segmentation masks.
        """
        img = read_dicom_series(image_path)
        metadata = {'spacing': list(np.abs(img.GetSpacing()[::-1]))}

        prediction = self.predictor.predict_single_npy_array(
            sitk.GetArrayFromImage(img)[None], 
            metadata, 
            None, 
            None, 
            False
        )

        return self._format_output(img, prediction)
    
if __name__ == '__main__':
    predictor = nnUNetPredictorWrapper(
        model_training_output_dir='nnunet_trained/iaslc_iter_1/nnUNetTrainer__nnUNetPlans__3d_fullres',
    )

    prediction = predictor.predict_single_dicom('')
    print(prediction)