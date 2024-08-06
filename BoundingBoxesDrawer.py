import easyocr
import cv2

class BoundingBoxesDrawer:
    def __init__(self):
        self.reader = easyocr.Reader(['it'], gpu=False)

    def analyzeImage(self, image_path):
        image = cv2.imread(image_path)
        result = self.reader.readtext(image_path)

        # Initialize the list to store extracted text and bounding boxes
        total_text = []
        bounding_boxes = []

        for (bbox, text, prob) in result:
            total_text.append(text)
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            br = (int(br[0]), int(br[1]))

            # Store bounding boxes
            bounding_boxes.append((tl, br))

        return image, ' '.join(total_text), bounding_boxes
    
    def drawBoxes(self, image, bounding_boxes):
        for i, (tl, br) in enumerate(bounding_boxes, 1):
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            cv2.putText(image, f"Box {i}", (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return image