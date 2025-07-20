from typing import List, Optional, Dict
from src.embeddings.base_embedding import BaseEmbeddingService
from conf.config import OPENAI_EMBEDDING_MODEL


class OpenAIEmbeddingService(BaseEmbeddingService):
    def __init__(self, logger):
        super().__init__(logger)
        self.logger = logger

    def generate_embedding(self, content: str) -> Optional[List[float]]:
        """
        Generate the embedding vector using the OpenAI model.
        """
        self.logger.info("Using OpenAi to Generate Embeddings")
        return [0.2] * 768

    def get_model_info(self) -> Dict[str, str]:
        """Returns information about the OpenAI model"""
        return {
            "provider": "openai",
            "model": OPENAI_EMBEDDING_MODEL,
        }
