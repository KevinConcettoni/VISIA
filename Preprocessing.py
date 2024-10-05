import numpy as np
import cv2

class ImagePreprocessor:
    def __init__(self, target_size=(64, 64)):
        self.target_size = target_size

    def preprocess(self, image):
        # Read the image
        img = cv2.imread(image)
        
        # Convert to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Adaptive Histogram Equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        equalized = clahe.apply(gray)
        
        # Noise reduction
        denoised = cv2.fastNlMeansDenoising(equalized, None, h=10, searchWindowSize=21, templateWindowSize=7)
        
        # Edge enhancement
        edges = cv2.Canny(denoised, 50, 150)
        
        # Dilation to connect adjacent edges
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Filling closed regions
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(dilated.shape, np.uint8)
        cv2.drawContours(mask, contours, -1, (255), -1)
        
        # Apply mask to original grayscale image
        result = cv2.bitwise_and(denoised, mask)
        
        # Resize while maintaining aspect ratio
        h, w = result.shape[:2]
        aspect = w / h
        if aspect > 1:
            new_w = self.target_size[0]
            new_h = int(new_w / aspect)
        else:
            new_h = self.target_size[1]
            new_w = int(new_h * aspect)
        resized = cv2.resize(result, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Padding to reach target size
        delta_w = self.target_size[0] - new_w
        delta_h = self.target_size[1] - new_h
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)
        padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
        
        # Normalization
        normalized = padded.astype(np.float32) / 255.0
        
        return normalized