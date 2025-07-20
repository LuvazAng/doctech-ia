from typing import List, Optional, Dict
from ollama import embeddings, EmbeddingsResponse
from src.embeddings.base_embedding import BaseEmbeddingService
from conf.config import OLLAMA_EMBEDDING_MODEL


class OllamaEmbeddingService(BaseEmbeddingService):
    """
    Concrete implementation of the EmbeddingService for Ollama models.
    """

    def __init__(self, logger):
        super().__init__(logger)
        self.logger = logger

    def generate_embedding(self, content: str) -> Optional[List[float]]:
        """
        Generate the embedding vector using the Ollama model.
        """
        try:
            response: EmbeddingsResponse = embeddings(
                model=OLLAMA_EMBEDDING_MODEL, prompt=content
            )

            embeddings_vector = response.model_dump().get("embedding")
            return embeddings_vector
        except IOError as e:
            self.logger.error("No se pudieron generar los embeddings: %s", e)
            return None

    def get_model_info(self) -> Dict[str, str]:
        """Returns information about the Ollama model"""
        return {
            "provider": "ollama",
            "model": OLLAMA_EMBEDDING_MODEL,
        }
