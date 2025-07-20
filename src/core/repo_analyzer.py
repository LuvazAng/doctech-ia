import os
import json
from conf.config import (
    IGNORED_DIRECTORIES,
    ALLOWED_FILE_EXTENSIONS,
    IGNORED_FILES,
    STRUCTURE_DIR,
)


class RepoAnalyzer:
    def __init__(self, logger):
        self.logger = logger

    def _is_file_allowed(self, filename: str) -> bool:
        """
        Checks if a file is allowed based on its extension and name.
        """
        _, ext = os.path.splitext(filename.lower())
        return ext in ALLOWED_FILE_EXTENSIONS and filename.lower() not in IGNORED_FILES

    def _filter_allowed_files(self, filenames: list[str]) -> list[str]:
        """
        Filters a list of filenames to include only allowed files.
        """
        return [f for f in filenames if self._is_file_allowed(f)]

    def _should_ignore_dir(self, dirname: str) -> bool:
        """
        Determines if a directory should be ignored.
        """
        return dirname in IGNORED_DIRECTORIES

    def _get_relative_path(self, full_path: str, base_dir: str) -> str:
        """
        Converts an absolute path to a relative Unix-style path.
        """
        rel_path = os.path.relpath(full_path, base_dir)
        return "/" if rel_path == "." else "/" + rel_path.replace("\\", "/")

    def _process_directory(
        self, dirpath: str, dirnames: list[str], filenames: list[str], base_dir: str
    ) -> tuple[str, list[str]]:
        """
        Processes a directory, filters subdirectories and files, and returns
        a relative path with allowed files.
        """
        dirnames[:] = [d for d in dirnames if not self._should_ignore_dir(d)]
        allowed_files = self._filter_allowed_files(filenames)

        if allowed_files:
            relative_path = self._get_relative_path(dirpath, base_dir)
            return relative_path, allowed_files
        return None, None

    def _build_structure(self, base_dir: str) -> dict:
        """
        Walks through the directory tree and builds a dictionary structure
        of valid directories and files.
        """
        structure = {}

        for dirpath, dirnames, filenames in os.walk(base_dir):
            rel_path, files = self._process_directory(
                dirpath, dirnames, filenames, base_dir
            )
            if rel_path and files:
                structure[rel_path] = files

        return structure

    def _save_structure_to_json(self, structure: dict, output_path: str):
        """
        Saves the directory structure as a JSON file.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(structure, f, indent=2, ensure_ascii=False)
            self.logger.info("Project structure saved in: %s", output_path)
        except (OSError, json.JSONDecodeError) as e:
            self.logger.error("Error saving the JSON file: %s", e)

    def analyze_and_export(self, cloned_repo_path: str, repo_name: str) -> str:
        """
        Analyzes the structure of the repository and exports it to a JSON file.
        """
        if not cloned_repo_path:
            self.logger.error("Invalid repository path: None received")
            raise ValueError("cloned_repo_path cannot be None")

        if not repo_name:
            self.logger.error("Invalid repository name: None received")
            raise ValueError("repo_name cannot be None")

        self.logger.info("Starting analysis of the repository")
        structure = self._build_structure(cloned_repo_path)

        output_path = os.path.join(STRUCTURE_DIR, f"{repo_name.lower()}.json")
        self._save_structure_to_json(structure, output_path)
        return output_path
