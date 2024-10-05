import cv2
import numpy as np
from ISegmentation import ISegmentation

class DefaultSegmentation(ISegmentation):
    def segment(self, image):
        # Convert float image to uint8
        image_uint8 = (image * 255).astype(np.uint8)

        # Convert the image to grayscale if it's not already
        if len(image_uint8.shape) == 3:
            gray = cv2.cvtColor(image_uint8, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_uint8

        # Apply thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        return binary