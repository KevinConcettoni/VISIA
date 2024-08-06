import os 
import json
from pathlib import Path

class ModelManager:
    def __init__(self, default_model_path, default_classes_json):
        self.models = {}
        self.custom_models_file = self.getCustomModelsFile()
        
        self.loadDefultModel(default_model_path, default_classes_json)
        self.loadCustomModels()

    def getCustomModelsFile(self):
        try:
            app_data_dir = Path.home() / '.image_analysis_app'
            app_data_dir.mkdir(parents=True, exist_ok=True)
            return app_data_dir / 'custom_models.json'
        except Exception as e:
            print(f"Error creating app data directory: {e}")
            return Path('custom_models.json')

    def loadDefultModel(self, default_model_path, default_classes_json):
        try:
            if not os.path.exists(default_model_path):
                raise FileNotFoundError(f"Default model not found at {default_model_path}")
            
            with open(default_classes_json, 'r') as f:
                classes_info = json.load(f)
            
            self.models['Default'] = {
                'path': default_model_path,
                'classes': classes_info['default'],
                'model_name': 'Default'
            }
            print("Default model loaded successfully.")
        except Exception as e:
            print(f"Error loading default model: {e}")

    def loadCustomModels(self):
        if self.custom_models_file.exists():
            try:
                with open(self.custom_models_file, 'r') as f:
                    custom_models = json.load(f)
                for model_name, model_info in custom_models.items():
                    self.models[model_name] = {
                        'path': model_info['path'],
                        'classes': model_info['classes'],
                        'model_name': model_name
                    }
                print("Custom models loaded successfully.")
            except Exception as e:
                print(f"Error loading custom models: {e}")

    def saveCustomModels(self):
        try:
            models_to_save = {
                model_name: {
                    'path': model_info['path'],
                    'classes': model_info['classes']
                }
                for model_name, model_info in self.models.items()
                if model_name != 'Default'
            }
            with open(self.custom_models_file, 'w') as f:
                json.dump(models_to_save, f, indent=2)
        except Exception as e:
            print(f"Error saving custom models: {e}")

    def addModel(self, name, model_path, classes):
        if name == 'Default':
            print("Cannot add a new model with the name 'Default'.")
            return

        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")

            self.models[name] = {
                'path': model_path,
                'classes': classes,
                'model_name': name
            }
            print(f"Model '{name}' added successfully.")
            self.saveCustomModels()
        except Exception as e:
            print(f"Error adding model: {e}")
            raise

    def getModel(self, name):
        return self.models.get(name)

    def getModelPath(self, name):
        model_info = self.models.get(name)
        return model_info['path'] if model_info else None

    def getModelClasses(self, name):
        model_info = self.models.get(name)
        return model_info['classes'] if model_info else None

    def getModelNames(self):
        return list(self.models.keys())

    def removeModel(self, name):
        if name == 'Default':
            print("Cannot remove the default model.")
            return
        if name in self.models:
            del self.models[name]
            self.saveCustomModels()
            print(f"Model '{name}' removed successfully.")
        else:
            print(f"Model '{name}' not found.")