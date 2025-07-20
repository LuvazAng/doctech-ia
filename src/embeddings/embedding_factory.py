from typing import Optional
from conf.config import EMBEDDING_PROVIDER
from src.embeddings.base_embedding import BaseEmbeddingService
from src.embeddings.providers.ollama_embedding import OllamaEmbeddingService
from src.embeddings.providers.openai_embedding import OpenAIEmbeddingService


class EmbeddingFactory:
    """Factory para crear instancias de servicios de embedding"""

    @staticmethod
    def get_embedding_service(logger) -> Optional[BaseEmbeddingService]:
        """
        Crea y retorna una instancia del servicio de embeddings basado en la configuración

        Args:
            logger: Logger para registrar información

        Returns:
            Optional[BaseEmbeddingService]: Instancia del servicio o None si hay error
        """
        provider = EMBEDDING_PROVIDER.lower()

        try:
            if provider == "ollama":
                service = OllamaEmbeddingService(logger)

            elif provider == "openai":
                service = OpenAIEmbeddingService(logger)
            else:
                logger.error("Provider not implemented: %s", provider)
                return None
            return service

        except ImportError as e:
            logger.error("Error importing supplier %s: %s", provider, e)
            return None
        except IOError as e:
            logger.error("Unexpected error creating embeddings service: %s", e)
            return None
