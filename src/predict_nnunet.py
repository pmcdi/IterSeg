import json
from typing import Tuple, Dict
from pathlib import Path

import numpy as np
import SimpleITK as sitk

from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
from nnunetv2.imageio.simpleitk_reader_writer import SimpleITKIO

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
                checkpoint_name='checkpoint_final.pth',
                use_folds=folds
        )

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

        labels = self.dataset_info['labels']
        data = {}

        for label, idx in labels.items():
            if idx == 0:
                continue

            label_image = sitk.GetImageFromArray(np.where(prediction == idx, prediction, 0))

            label_image.SetSpacing(metadata['sitk_stuff']['spacing'])
            label_image.SetOrigin(metadata['sitk_stuff']['origin'])
            label_image.SetDirection(metadata['sitk_stuff']['direction'])

            data[label] = label_image

        return data
    
if __name__ == '__main__':
    predictor = nnUNetPredictorWrapper(
        model_training_output_dir='',
    )

    prediction = predictor.predict_from_single_image('')
    print(prediction)