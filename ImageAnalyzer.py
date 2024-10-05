import tensorflow as tf
import numpy as np
import cv2
from BoundingBoxesDrawer import BoundingBoxesDrawer
from DefaultSegmentation import DefaultSegmentation
from IModel import IModel
from Preprocessing import ImagePreprocessor

class ImageAnalyzer(IModel):
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.model = None
        self.class_names = []
        self.box_drawer = BoundingBoxesDrawer()
        self.segmentator = DefaultSegmentation()
        self.preprocessor = ImagePreprocessor(target_size=(64, 64))

    def setModel(self, model_name):
        model_info = self.model_manager.getModel(model_name)
        if model_info is None:
            raise ValueError(f"Model '{model_name}' not found.")
        
        self.model = tf.keras.models.load_model(model_info['path'])
        self.class_names = model_info['classes']
        print(f"Model '{model_name}' loaded successfully with classes: {self.class_names}")

    def preprocessImage(self, image):
        # Preprocess the image
        preprocessed = self.preprocessor.preprocess(image)
        
        # Segment the preprocessed image
        segmented = self.segmentator.segment(preprocessed)
        
        # Add batch dimension
        segmented = np.expand_dims(segmented, axis=0)
        
        return segmented

    def analyze(self, image_path):
        if self.model is None:
            raise ValueError("Model has not been set.")

        original_image, text, bounding_boxes = self.box_drawer.findBoundingBoxes(image_path)

        predictions = []
        for i, (tl, br) in enumerate(bounding_boxes, 1):
            x_min, y_min = tl
            x_max, y_max = br
            extracted_bb = original_image[y_min:y_max, x_min:x_max]
            if extracted_bb.size == 0:
                continue
            
            # Save the extracted bounding box as a temporary image file
            temp_bb_path = f"temp_bb_{i}.jpg"
            cv2.imwrite(temp_bb_path, extracted_bb)
            
            # Process the temporary image file
            processed_bb = self.preprocessImage(temp_bb_path)
            
            # Remove the temporary file
            import os
            os.remove(temp_bb_path)
            
            prediction = self.model.predict(processed_bb)
            label_index = np.argmax(prediction, axis=1)[0]
            label = self.class_names[label_index]
            confidence = float(prediction[0][label_index])
            predictions.append({"box": i, "label": label, "confidence": confidence})

        annotated_image = self.box_drawer.drawBoxes(original_image, bounding_boxes)

        return annotated_image, text, predictions, bounding_boxes