import time
from requests.exceptions import RequestException
from src.core.repo_manager import RepoManager
from src.core.repo_analyzer import RepoAnalyzer
from src.core.repo_code_splitter import RepoCodeSplitter


class Orchestrator:
    def __init__(self, logger=None):
        """
        Initializes the Orchestrator instance.

        Args:
            logger (logging.Logger, optional): Logger instance for logging events.
        """
        self.logger = logger
        self.repo_manager = RepoManager(logger)
        self.repo_analyzer = RepoAnalyzer(logger)
        self.repo_code_splitter = RepoCodeSplitter(logger)

    def proccessing_repo(self, url_repo: str, token: str = None, username: str = None):
        """
        Coordinates the full pipeline:
        - Clones the repository
        - Analyzes its structure
        - Processes the code for embedding

        Args:
            url_repo (str): URL of the GitHub repository.
            token (str, optional): GitHub token if authentication is needed.
            username (str, optional): GitHub username if authentication is needed.
        """
        try:
            self.logger.info("Starting process. It may take a while...")

            cloned_repo_path, repo_name = self.repo_manager.get_repo(
                url_repo, token, username
            )
            self.logger.info(
                "Repository name: %s, Origin: %s", repo_name, cloned_repo_path
            )

            start_time = time.time()

            output_json_path = self.repo_analyzer.analyze_and_export(
                cloned_repo_path, repo_name
            )
            self.logger.info("Structure exported to: %s", output_json_path)

            self.repo_code_splitter.process_files(
                repo_name, cloned_repo_path, output_json_path
            )

            end_time = time.time()
            elapsed_time = end_time - start_time
            self.logger.info(
                "The processing of embeddings has concluded. Elapsed time: %.2f seconds",
                elapsed_time,
            )

        except ValueError as ve:
            self.logger.error("Invalid URL or malformed parameter: %s", ve)

        except RequestException as re:
            self.logger.error("Network issue while accessing repository: %s", re)
            raise ConnectionError("Network error during repository download") from re

        except Exception:
            self.logger.exception("Unexpected error during processing")
            raise
