import sys
from PyQt5.QtWidgets import QApplication
from UserInterface import UserInterface
from ModelManager import ModelManager
from ImageAnalyzer import ImageAnalyzer
from ResultManager import ResultManager

def main():
    app = QApplication(sys.argv)
    default_model = 'Models/Default.keras'
    default_classes = 'class_names.json'
    model_manager = ModelManager(default_model, default_classes)
    result_manager = ResultManager()
    image_analyzer = ImageAnalyzer(model_manager)

    ui = UserInterface(model_manager, image_analyzer, result_manager)
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()