from abc import ABC, abstractmethod
from typing import Dict, Any
import Image

class IModel(ABC):
    @abstractmethod
    def analyze(self, image: Image):
        pass