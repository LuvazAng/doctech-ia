"""Git handler module for managing temporary repositories"""

import os
import re
import socket
from urllib.parse import urlparse, urlunparse
import git
import git.exc
from conf.config import REPOS_DIR


class RepoManager:
    """Temporary repository handler class"""

    def __init__(self, logger):
        self.logger = logger

    def _identify_platform(self, hostname: str) -> str:
        """Detect the platform (GitHub, GitLab, Bitbucket, Azure, etc.)"""
        if "github.com" in hostname:
            return "github"
        elif "gitlab.com" in hostname:
            return "gitlab"
        elif "bitbucket.org" in hostname:
            return "bitbucket"
        elif "dev.azure.com" in hostname:
            return "azure"
        elif "gitea" in hostname:
            return "gitea"

    def _build_authentication_url(
        self, url_repo: str, token: str = None, username: str = None
    ) -> str:
        """Build the URL with authentication, according to the provider"""
        parsed_url = urlparse(url_repo)
        hostname = parsed_url.netloc
        platform = self._identify_platform(hostname)

        if not token:
            self.logger.info("No token provided. Using URL as is.")
            return url_repo

        self.logger.info("Using token for authentication. Plaform: %s", platform)

        if platform in ["bitbucket", "azure"]:
            if not username:
                raise ValueError(
                    f"{platform.capitalize()} requires a username and token for authentication."
                )
            new_netloc = f"{username}:{token}@{hostname}"
        elif platform in ["github", "gitlab", "gitea"]:
            new_netloc = f"{(username + ':' if username else '')}{token}@{hostname}"
        else:
            self.logger.warning(
                "Unknown platform %s. Using token only format.", hostname
            )
            new_netloc = f"{token}@{hostname}"

        return urlunparse(
            (
                parsed_url.scheme,
                new_netloc,
                parsed_url.path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )

    def _extract_repo_name(self, url: str) -> str:
        """Extract repository name from SSH or HTTPS URL"""
        url = url.rstrip("/")

        ssh_match = re.match(
            r"(?:git@|ssh://git@)([^:/]+)[:/](.+?)(?:\.git)?(?:\?.*)?$", url
        )
        if ssh_match:
            path = ssh_match.group(2)
            return os.path.splitext(path)[0].split("/")[-1]

        # HTTPS-style
        parsed = urlparse(url)
        path = parsed.path

        # Remove .git and query string
        if path.endswith(".git"):
            path = path[:-4]
        path = path.split("?")[0]

        return path.strip("/").split("/")[-1]

    def _is_valid_url(self, url: str) -> bool:
        """Check if a given string is a valid HTTP(S) or SSH Git URL."""
        if not url or not isinstance(url, str):
            return False

        parsed = urlparse(url)

        # Valida URLs HTTP/HTTPS
        if parsed.scheme in ["http", "https"] and parsed.netloc and parsed.path:
            return True

        # Valida URLs SSH estilo: git@github.com:user/repo.git
        ssh_pattern = r"^(git@|ssh://git@)[\w.-]+[:/][\w./-]+(\.git)?$"
        if re.match(ssh_pattern, url):
            return True

        return False

    def get_repo(self, url_repo: str, token: str = None, username: str = None):
        """Clone or update a temporary repository from the URL"""
        if not self._is_valid_url(url_repo):
            self.logger.error("Invalid repository URL: '%s'", url_repo)
            return [None, None]

        try:
            url = self._build_authentication_url(url_repo, token, username)
            repo_name = self._extract_repo_name(url_repo)
            repo_dest_path = REPOS_DIR / repo_name

            if repo_dest_path.exists():
                self.logger.info(
                    "Repository '%s' already exists. Performing git pull", repo_name
                )
                repo = git.Repo(repo_dest_path)
                repo.remotes.origin.pull()
                self.logger.info("Repository '%s' updated successfully", repo_name)
            else:
                repo = git.Repo.clone_from(url, str(repo_dest_path))
                self.logger.info("Repository '%s'", repo_name)
            return [repo_dest_path, repo_name]

        except git.exc.GitCommandError:
            self.logger.error(
                "The host cannot be resolved (possible network or DNS issue)"
            )
            return [None, None]  # o `raise` si quieres propagarlo igual

        except git.exc.GitCommandNotFound as gcnf:
            self.logger.error(
                "Git executable not found. Check PATH or GIT_PYTHON_GIT_EXECUTABLE.: %s",
                gcnf,
            )
            return [None, None]

        except socket.gaierror as net_err:
            self.logger.error("Error de red al intentar resolver el host: %s", net_err)
            return [None, None]

        except Exception as e:
            self.logger.error("Unexpected error: %s", e)
            raise
