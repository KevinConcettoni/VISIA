from abc import ABC, abstractmethod
from typing import Dict, Any
import Image

class ISegmentation(ABC):
    @abstractmethod
    def segment(self, image: Image) -> Image:
        pass