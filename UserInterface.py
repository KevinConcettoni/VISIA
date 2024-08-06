import os
import cv2
import json
from PyQt5.QtWidgets import (
    QMessageBox, QInputDialog, QWidget, QPushButton, QVBoxLayout, QLabel,
    QFileDialog, QComboBox, QScrollArea, QDialog, QListWidgetItem, QHBoxLayout,
    QMainWindow, QToolBar, QStatusBar, QTabWidget, QListWidget, QSplitter, QFrame, QApplication
)
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, QSize
from Image import Image

class UserInterface(QMainWindow):
    def __init__(self, model_manager, image_analyzer, result_manager):
        super().__init__()
        self.model_manager = model_manager
        self.image_analyzer = image_analyzer
        self.result_manager = result_manager
        self.current_images = []
        self.initUI()

    def initUI(self):
        self.setWindowProperties()
        self.createCentralWidget()
        self.createToolbar()
        self.createStatusBar()
        self.applyStyles()

    def setWindowProperties(self):
        self.setWindowTitle('Image Analyzer')
        self.setGeometry(100, 100, 1200, 800)

    def createCentralWidget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.createSplitter())

    def createSplitter(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.createLeftPanel())
        splitter.addWidget(self.createRightPanel())
        splitter.setSizes([250, 950])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        return splitter

    def createLeftPanel(self):
        panel = QFrame(self)
        panel.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("Image List", alignment=Qt.AlignCenter))
        layout.addWidget(self.createImageList())
        return panel

    def createImageList(self):
        self.image_list = QListWidget()
        self.image_list.setMaximumWidth(250)
        self.image_list.itemClicked.connect(self.displaySelectedImage)
        return self.image_list

    def createRightPanel(self):
        panel = QTabWidget()
        panel.setDocumentMode(True)
        panel.setTabPosition(QTabWidget.North)
        panel.addTab(self.createImageView(), "Image View")
        panel.addTab(self.createResultsView(), "Results")
        return panel

    def createImageView(self):
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.mousePressEvent = self.onImageClick
        scroll_area = QScrollArea(widgetResizable=True)
        scroll_area.setWidget(self.image_label)
        return scroll_area

    def createResultsView(self):
        self.results_view = QScrollArea(widgetResizable=True)
        return self.results_view

    def createToolbar(self):
        toolbar = QToolBar(movable=False)
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        self.addToolbarButtons(toolbar)
        self.addModelControls(toolbar)
        self.addResultControls(toolbar)

    def addToolbarButtons(self, toolbar):
        self.addToolbarButton(toolbar, 'Icons/load_image.png', 'Load Image', self.loadImage)
        self.addToolbarButton(toolbar, 'Icons/load_folder.png', 'Load Folder', self.loadFolder)
        toolbar.addSeparator()

    def addModelControls(self, toolbar):
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.model_manager.getModelNames())
        self.model_combo.setFixedWidth(150)
        toolbar.addWidget(self.model_combo)
        self.addToolbarButton(toolbar, 'Icons/analyze_image.png', 'Analyze', self.analyzeImages)
        toolbar.addSeparator()
        self.addToolbarButton(toolbar, 'Icons/add_model.png', 'Add Model', self.loadModel)
        self.addToolbarButton(toolbar, 'Icons/remove_model.png', 'Remove Model', self.removeCustomModel)
        toolbar.addSeparator()

    def addResultControls(self, toolbar):
        self.addToolbarButton(toolbar, 'Icons/clear.png', 'Clear', self.clear)
        self.addToolbarButton(toolbar, 'Icons/load_results.png', 'Load Results', self.loadResults)
        self.addToolbarButton(toolbar, 'Icons/download_results.png', 'Download Results', self.downloadResults)

    def addToolbarButton(self, toolbar, icon, tooltip, callback):
        button = QPushButton(QIcon(icon), "")
        button.setIconSize(QSize(24, 24))
        button.clicked.connect(callback)
        button.setToolTip(tooltip)
        button.setFixedSize(QSize(40, 40))
        toolbar.addWidget(button)

    def createStatusBar(self):
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def applyStyles(self):
        self.setColorScheme()
        self.setStyleSheet(self.getStyleSheet())

    def setColorScheme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)

    def getStyleSheet(self):
        return """
        QMainWindow, QWidget { background-color: #f0f0f0; }
        QToolBar { border: none; background-color: #e0e0e0; spacing: 6px; padding: 3px; }
        QPushButton { background-color: #b0b0b0; color: white; border: none; padding: 5px; border-radius: 3px; }
        QPushButton:hover { background-color: #c0c0c0; }
        QPushButton:pressed { background-color: #a0a0a0; }
        QComboBox, QListWidget { border: 1px solid #c0c0c0; border-radius: 3px; padding: 5px; }
        QComboBox { min-width: 6em; }
        QTabWidget::pane { border: 1px solid #c0c0c0; border-radius: 3px; }
        QTabBar::tab { background-color: #e0e0e0; border: 1px solid #c0c0c0; border-bottom-color: #c0c0c0;
                    border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 8ex; padding: 5px; }
        QTabBar::tab:selected, QTabBar::tab:hover { background-color: #f0f0f0; }
        QTabBar::tab:selected { border-color: #9B9B9B; border-bottom-color: #f0f0f0; }
        QStatusBar { background-color: #e0e0e0; }
        """

    def loadImage(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.addImageToAnalysis(file_path)

    def loadFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.bmp')):
                    self.addImageToAnalysis(os.path.join(folder_path, filename))

    def addImageToAnalysis(self, image_path):
        image = Image(image_path)
        self.current_images.append(image)
        self.addImageToList(image)
        if len(self.current_images) == 1:
            self.displayImage(image)

    def addImageToList(self, image):
        item = QListWidgetItem(os.path.basename(image.path))
        item.setData(Qt.UserRole, image)
        self.image_list.addItem(item)

    def displaySelectedImage(self, item):
        image = item.data(Qt.UserRole)
        self.displayImage(image)
        self.displayAnalysisResult(image)

    def displayImage(self, image):
        pixmap = self.getPixmap(cv2.imread(image.path))
        self.image_label.setPixmap(pixmap)
        self.fixImageToView()

    def displayAnalysisResult(self, image):
        result = self.result_manager.getResult(image.path)
        if result:
            original_image = cv2.imread(image.path)
            analyzed_image = self.drawBoundingBoxes(original_image.copy(), result['predictions'], result['bounding_boxes'])
            self.displayAnalyzedImage(original_image, analyzed_image, result['predictions'], result['bounding_boxes'])

    def fixImageToView(self):
        if self.image_label.pixmap():
            available_width = self.image_label.width() - 20
            available_height = self.image_label.height() - 20
            self.image_label.setPixmap(
                self.image_label.pixmap().scaled(
                    available_width,
                    available_height,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

    def onImageClick(self, event):
        if self.image_label.pixmap():
            self.showEnlargedImage(self.image_label.pixmap())

    def showEnlargedImage(self, pixmap):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enlarged Image")
        layout = QVBoxLayout(dialog)
        scroll = QScrollArea(widgetResizable=True)
        enlarged_label = QLabel()
        
        screen_rect = QApplication.desktop().screenGeometry()
        max_width = int(screen_rect.width() * 0.8)
        max_height = int(screen_rect.height() * 0.8)
        
        enlarged_pixmap = pixmap.scaled(
            max_width,
            max_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        enlarged_label.setPixmap(enlarged_pixmap)
        scroll.setWidget(enlarged_label)
        layout.addWidget(scroll)
        dialog.resize(enlarged_pixmap.width() + 30, enlarged_pixmap.height() + 30)
        dialog.exec_()

    def analyzeImages(self):
        selected_model = self.model_combo.currentText()
        try:
            self.image_analyzer.setModel(selected_model)
        except Exception as e:
            self.showError(f"Failed to load model: {str(e)}")
            return

        total_images = len(self.current_images)
        for i, image in enumerate(self.current_images, 1):
            try:
                self.analyzeImage(image, selected_model)
                self.updateStatus(f"Analyzed {i}/{total_images} images")
            except Exception as e:
                self.showError(f"Error analyzing image {image.path}: {str(e)}")

        self.showInfo(f"Analysis complete. Analyzed {total_images} images.")

    def analyzeImage(self, image, model_name):
        original_image = cv2.imread(image.path)
        annotated_image, text, predictions, bounding_boxes = self.image_analyzer.analyze(image.path)
        self.result_manager.addResult(image.path, model_name, text, predictions, bounding_boxes)
        self.displayAnalyzedImage(original_image, annotated_image, predictions, bounding_boxes)

    def displayAnalyzedImage(self, original_image, analyzed_image, predictions, bounding_boxes):
        result_widget = QWidget()
        layout = QVBoxLayout(result_widget)
        layout.addWidget(self.createImageComparisonWidget(original_image, analyzed_image))
        layout.addWidget(self.createResultTextWidget(predictions, bounding_boxes))
        self.results_view.setWidget(result_widget)

    def createImageComparisonWidget(self, original_image, analyzed_image):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        for image, label_text in [(original_image, "Original"), (analyzed_image, "Analyzed")]:
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.addWidget(QLabel(label_text))
            image_label = QLabel()
            pixmap = self.getPixmap(image)
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            # Change the fixed size
            image_label.setFixedSize(300, 300)
            image_label.mousePressEvent = lambda event, img=image: self.showEnlargedImage(self.getPixmap(img))
            container_layout.addWidget(image_label)
            container_layout.addWidget(QLabel("Click to enlarge"))
            layout.addWidget(container)
        return widget

    def createResultTextWidget(self, predictions, bounding_boxes):
        result_text = "Predictions:\n"
        for i, (pred, bbox) in enumerate(zip(predictions, bounding_boxes), 1):
            result_text += f"Box {i}: {pred['label']} (Confidence: {pred['confidence']:.2f})\n"
            result_text += f"  Coordinates: Top-Left {bbox[0]}, Bottom-Right {bbox[1]}\n"
        label = QLabel(result_text)
        label.setWordWrap(True)
        return label

    def getPixmap(self, image, size=None):
        if len(image.shape) == 2:
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        
        pixmap = QPixmap.fromImage(q_image)
        if size:
            return pixmap.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    def clear(self):
        self.current_images.clear()
        self.image_list.clear()
        self.image_label.clear()
        self.results_view.setWidget(QWidget())
        self.result_manager.clearResult()
        self.updateStatus("All data cleared")

    def loadModel(self):
        model_file = self.getFileFromDialog("Select Model File", "Model Files (*.keras *.h5)")
        if not model_file:
            return

        classes_file = self.getFileFromDialog("Select Classes JSON File", "JSON Files (*.json)")
        if not classes_file:
            return

        self.processModelFiles(model_file, classes_file)

    def getFileFromDialog(self, title, file_filter):
        return QFileDialog.getOpenFileName(self, title, "", file_filter)[0]

    def processModelFiles(self, model_file, classes_file):
        try:
            with open(classes_file, 'r') as f:
                classes_info = json.load(f)
            
            model_name, ok = QInputDialog.getText(self, "Model Name", "Enter a name for this model:")
            if ok and model_name:
                classes = classes_info.get(model_name, [])
                if not classes:
                    raise ValueError(f"No classes found for model '{model_name}' in the JSON file.")
                
                self.model_manager.addModel(model_name, model_file, classes)
                self.updateModelCombo()
                self.updateStatus(f"Model '{model_name}' added successfully")
            else:
                raise ValueError("Model name is required.")
        except Exception as e:
            self.showError(f"Failed to load model: {str(e)}")

    def removeCustomModel(self):
        selected_model = self.model_combo.currentText()
        if selected_model == 'Default':
            self.showWarning("Cannot remove the default model.")
        else:
            if self.showConfirmDialog("Remove Model", f"Are you sure you want to remove '{selected_model}'?"):
                self.model_manager.removeModel(selected_model)
                self.updateModelCombo()
                self.updateStatus(f"Model '{selected_model}' removed successfully")

    def updateModelCombo(self):
        current_text = self.model_combo.currentText()
        self.model_combo.clear()
        self.model_combo.addItems(self.model_manager.getModelNames())
        index = self.model_combo.findText(current_text)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)

    def downloadResults(self):
        results = self.result_manager.getAllResult()
        if not results:
            self.showWarning("There are no results to download.")
            return

        save_folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save Results")
        if save_folder:
            folder_name = self.getFolderNameFromUser()
            if folder_name:
                self.saveResults(save_folder, folder_name, results)

    def getFolderNameFromUser(self):
        folder_name, ok = QInputDialog.getText(self, "Folder Name", "Enter a name for the results folder:")
        return folder_name if ok and folder_name else None

    def saveResults(self, save_folder, folder_name, results):
        result_folder = os.path.join(save_folder, folder_name)
        if os.path.exists(result_folder):
            if not self.showConfirmDialog("Folder Exists", f"The folder '{folder_name}' already exists. Do you want to overwrite it?"):
                return

        os.makedirs(result_folder, exist_ok=True)
        saved_results = {}

        for image_path, result in results.items():
            self.saveAnalyzedImage(image_path, result, result_folder, saved_results)

        self.saveMetadata(result_folder, saved_results)
        self.showInfo(f"Results saved to {result_folder}")

    def saveAnalyzedImage(self, image_path, result, result_folder, saved_results):
        image = cv2.imread(image_path)
        if image is None:
            return

        image = self.drawBoundingBoxes(image, result['predictions'], result['bounding_boxes'])
        
        image_filename = f"annotated_{os.path.basename(image_path)}"
        image_save_path = os.path.join(result_folder, image_filename)
        cv2.imwrite(image_save_path, image)

        text_filename = f"result_{os.path.basename(image_path)}.txt"
        text_save_path = os.path.join(result_folder, text_filename)
        self.saveResultText(text_save_path, image_path, result)

        saved_results[image_filename] = {
            'image_path': image_save_path,
            'text_path': text_save_path,
            'original_path': image_path,
            'model': result['model'],
            'classes': self.model_manager.getModelClasses(result['model']),
            'predictions': result['predictions'],
            'bounding_boxes': result['bounding_boxes']
        }

    def saveResultText(self, save_path, image_path, result):
        with open(save_path, 'w') as f:
            f.write(f"Image: {os.path.basename(image_path)}\n")
            f.write(f"Model: {result['model']}\n")
            f.write(f"Classes: {', '.join(self.model_manager.getModelClasses(result['model']))}\n\n")
            f.write("Predictions:\n")
            for i, (pred, bbox) in enumerate(zip(result['predictions'], result['bounding_boxes']), 1):
                f.write(f"  Box {i}: {pred['label']} (Confidence: {pred['confidence']:.2f})\n")
                f.write(f"    Coordinates: Top-Left {bbox[0]}, Bottom-Right {bbox[1]}\n")

    def saveMetadata(self, result_folder, saved_results):
        json_path = os.path.join(result_folder, "analysis_metadata.json")
        with open(json_path, 'w') as jsonfile:
            json.dump(saved_results, jsonfile, indent=2)

    def loadResults(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Results Folder")
        if folder_path:
            self.loadResultsFromFolder(folder_path)

    def loadResultsFromFolder(self, folder_path):
        json_path = os.path.join(folder_path, "analysis_metadata.json")
        if not os.path.exists(json_path):
            self.showError("Invalid results folder. Metadata file not found.")
            return

        try:
            with open(json_path, 'r') as jsonfile:
                loaded_results = json.load(jsonfile)
            self.clear()
            self.displayLoadedResults(loaded_results, folder_path)
            self.showInfo("Results loaded successfully.")
        except Exception as e:
            self.showError(f"Failed to load results: {str(e)}")

    def displayLoadedResults(self, loaded_results, base_folder):
        for image_filename, result in loaded_results.items():
            analyzed_image_path = os.path.join(base_folder, os.path.basename(result['image_path']))
            original_image_path = result['original_path']
            
            image = Image(original_image_path)
            self.current_images.append(image)
            self.addImageToList(image)

            self.loadAndDisplayResult(image, analyzed_image_path, result)

    def loadAndDisplayResult(self, image, analyzed_image_path, result):
        try:
            original_image = cv2.imread(image.path)
            analyzed_image = cv2.imread(analyzed_image_path)
            if original_image is None or analyzed_image is None:
                raise ValueError("Could not load image from path.")
            
            self.result_manager.addResult(
                image.path,
                result['model'],
                "",
                result['predictions'],
                result['bounding_boxes']
            )
            
            if image == self.current_images[0]:
                self.displayAnalyzedImage(original_image, analyzed_image, result['predictions'], result['bounding_boxes'])
        except Exception as e:
            self.showError(f"Error displaying image {image.path}: {str(e)}")

    def drawBoundingBoxes(self, image, predictions, bounding_boxes):
        for i, (pred, bbox) in enumerate(zip(predictions, bounding_boxes), 1):
            tl, br = bbox
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            label = f"Box {i}: {pred['label']}"
            cv2.putText(image, label, (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return image

    def showConfirmDialog(self, title, message):
        reply = QMessageBox.question(self, title, message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def showError(self, message):
        QMessageBox.critical(self, "Error", message)

    def showWarning(self, message):
        QMessageBox.warning(self, "Warning", message)

    def showInfo(self, message):
        QMessageBox.information(self, "Information", message)

    def updateStatus(self, message, timeout=3000):
        self.statusBar.showMessage(message, timeout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fixImageToView()