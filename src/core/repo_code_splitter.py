"""Important imports of the project"""

import os
import json
from typing import Optional, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.embeddings.embedding_factory import EmbeddingFactory
from src.db.vdb_manager import VectorDatabase
from conf.config import CHUNK_SIZE_CODE, CHUNK_OVERLAP_CODE


class RepoCodeSplitter:
    """Class to process the content of the code files"""

    def __init__(self, logger):
        self.logger = logger
        self.embedding_service = EmbeddingFactory.get_embedding_service(self.logger)
        self.vecto_db = VectorDatabase(logger)

    def _load_repo_structure(self, json_structure_path: str):
        """Load the repository structure from a JSON file"""
        self.logger.debug("Processing files from the JSON %s", json_structure_path)
        try:
            with open(json_structure_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.error("The JSON file was not found in %s", json_structure_path)
            return {}
        except json.JSONDecodeError:
            self.logger.error("The JSON file does not have a valid format.")
            return {}
        except IOError as e:
            self.logger.error("Unexpected error while loading the JSON: %s", e)

    def _get_file_path(
        self, cloned_repo_path: str, relative_path: str, filename: str
    ) -> str:
        """Build the full path of a file."""
        actual_dir_path = os.path.join(cloned_repo_path, relative_path.lstrip("/"))
        return os.path.join(actual_dir_path, filename)

    def _read_file_content(self, full_file_path: str) -> Optional[str]:
        """Read the content of a file."""
        self.logger.info("Opening and processing file")
        try:
            with open(full_file_path, "r", encoding="utf-8") as file_content:
                return file_content.read()
        except IOError as e:
            self.logger.error("Unexpected error while loading the JSON: %s", e)
            return None

    def _build_final_filename(self, relative_path: str, filename: str) -> str:
        if relative_path == "/":
            final_filename = filename
        else:
            final_filename = os.path.join(relative_path.lstrip("/"), filename)
        return final_filename.replace("\\", "/")

    def _create_text_splitter(self, content: str) -> List[str]:
        """
        Divide the content given in fragments using recursivehactertextsplitter.

        Args:
            content (str): The content of the file to be divided.

        Returns:
            List[str]: List of text fragments.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE_CODE,
            chunk_overlap=CHUNK_OVERLAP_CODE,
            length_function=len,
        )
        return text_splitter.split_text(content)

    def _generate_embeddings(self, content: str) -> Optional[List[float]]:
        """
        Generate the embedding vector for the given content using the injected service.
        """
        if not self.embedding_service:
            self.logger.error("Embeddings service not available")
            return None

        if not content or not content.strip():
            self.logger.warning("Empty content, embedding cannot be generated")
            return None

        try:
            embedding = self.embedding_service.generate_embedding(content)

            if embedding:
                return embedding
            else:
                self.logger.error("The embedding could not be generated.")
                return None

        except IOError as e:
            self.logger.error("Unexpected error generating embedding: %s", e)
            return None

    def process_files(
        self, repo_name: str, cloned_repo_path: str, json_structure_path: str
    ):
        """
        Coordinate reading of the structured JSON and the processing of the
        corresponding code files, storing embeddings into the vector DB.
        """
        repo_structure = self._load_repo_structure(json_structure_path)
        if not repo_structure:
            self.logger.error(
                "The repository structure could not be loaded or is empty."
            )
            return

        model_info = self.embedding_service.get_model_info()
        self.logger.info(
            "You are using the service: '%s' with the model: '%s'",
            model_info.get("provider").capitalize(),
            model_info.get("model"),
        )

        if not self.vecto_db.setup_database(table_name=repo_name):
            self.logger.error("Database setup failed for table: %s", repo_name)
            return

        for relative_path, files in repo_structure.items():
            for filename in files:
                full_file_path = self._get_file_path(
                    cloned_repo_path, relative_path, filename
                )
                if not os.path.exists(full_file_path):
                    self.logger.error("File not found: %s", full_file_path)
                    continue

                content = self._read_file_content(full_file_path)
                if content is None:
                    continue

                final_filename = self._build_final_filename(relative_path, filename)

                chunks = self._create_text_splitter(content)
                if not chunks:
                    self.logger.warning(
                        "No se generaron chunks para: %s", final_filename
                    )
                    continue

                for idx, chunk in enumerate(chunks):
                    embedding_vector = self._generate_embeddings(chunk)

                    if embedding_vector:
                        self.logger.info(
                            "Embedding generated for: %s [chunk %d]",
                            final_filename,
                            idx,
                        )
                        success = self.vecto_db.insert_embedding(
                            filename=final_filename,
                            content=chunk,
                            embedding=embedding_vector,
                            chunk_order=idx,
                            table_name=repo_name,
                        )
                        if not success:
                            self.logger.error(
                                "Failed when inserting chunk %d of %s",
                                idx,
                                final_filename,
                            )
                    else:
                        self.logger.warning(
                            "Embedding could not be generated for: %s [chunk %d]",
                            final_filename,
                            idx,
                        )
