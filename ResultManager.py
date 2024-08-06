class ResultManager:
    def __init__(self):
        self.results = {}

    def addResult(self, image_path, model, text, predictions, bounding_boxes):
        self.results[image_path] = {
            'model': model,
            'text': text,
            'predictions': predictions,
            'bounding_boxes': bounding_boxes
        }

    def getResult(self, image_path):
        return self.results.get(image_path)

    def getAllResult(self):
        return self.results

    def clearResult(self):
        self.results.clear()