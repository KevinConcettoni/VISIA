import cv2

class Image:
    def __init__(self, path):
        self.path = path
        self.data = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    def getData(self):
        return self.data # Matrice di pixel