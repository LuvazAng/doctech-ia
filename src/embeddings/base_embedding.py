from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class BaseEmbeddingService(ABC):
    """Abstract base class for embedding services"""

    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    def generate_embedding(self, content: str) -> Optional[List[float]]:
        """
        Generate an embedding for the given text

        Args:
            content (str): Text to generate the embedding

        Returns:
            Optional[List[float]]: Embedding vector or None if there is an error
        """

    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        """
        Retorna información del modelo utilizado

        Returns:
            Dict[str, str]: Información del modelo (nombre, proveedor, etc.)
        """
