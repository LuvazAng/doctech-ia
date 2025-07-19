"""
Class Orchestrator

This module defines the Orchestrator class, which is responsible for coordinating
the retrieval and processing of repositories using the RepoManager class.
"""

from requests.exceptions import RequestException
from src.core.repo_manager import RepoManager
from src.core.repo_analyzer import RepoAnalyzer


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

    def proccessing_repo(self, url_repo: str, token: str = None, username: str = None):
        """
        Coordinates the full pipeline:
        - Clones the repository
        - Analyzes its structure
        - Processes the code for embedding (coming soon) <{:{D

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

            # Analyze the repo and export its structure
            output_json_path = self.repo_analyzer.analyze_and_export(
                cloned_repo_path, repo_name
            )
            self.logger.info("Structure exported to: %s", output_json_path)

        except ValueError as ve:
            self.logger.error("Invalid URL or malformed parameter: %s", ve)

        except RequestException as re:
            self.logger.error("Network issue while accessing repository: %s", re)
            raise ConnectionError("Network error during repository download") from re

        except Exception:
            self.logger.exception("Unexpected error during processing")
            raise
