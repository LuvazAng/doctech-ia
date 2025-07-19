"""Configuration file for the application."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# CONFIGURACIÓN DE POSGRESQL
POSGRESQL_DB_NAME = os.getenv("POSGRESQL_DB_NAME")
POSGRESQL_DB_USER = os.getenv("POSGRESQL_DB_USER")
POSGRESQL_DB_PSW = os.getenv("POSGRESQL_DB_PSW")
POSGRESQL_DB_HOST = os.getenv("POSGRESQL_DB_HOST")
POSGRESQL_DB_PORT = os.getenv("POSGRESQL_DB_PORT")

# MODELS CONFIGURATION
OLLAMA_HOST = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# EMBEDDING CONFIGURATION
EMBEDDING_MODEL_PROVIDER = os.getenv(
    "EMBEDDING_MODEL_PROVIDER", "ollama"
)  # 'ollama', 'openai'
OLLAMA_EMBEDDING_MODEL = os.getenv(
    "OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"
)  # Ollama embedding model
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Chunking configuration
CODE_CHUNK_SIZE = 2000
CODE_CHUNK_OVERLAP = 200
MD_CHUNK_SIZE = 1500
MD_CHUNK_OVERLAP = 150

# File and directory configurations
IGNORED_DIRECTORIES = {
    ".git",
    ".svn",
    ".hg",
    ".bzr",
    "__pycache__",
    "node_modules",
    "bower_components",
    "jspm_packages",
    "venv",
    ".venv",
    "env",
    "virtualenv",
    ".vscode",
    "build",
    "dist",
    "bin",
    "obj",
    ".idea",
    ".ipynb_checkpoints",
    "target",
    "out",
}
IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "npm-debug.log",
    "yarn-error.log",
    "package-lock.json",
    "yarn.lock",
    ".prettierrc.json",
    "eslint.config.js",
    "jsconfig.json",
    "package.json",
    "pnpm-lock.yaml",
    "npm-shrinkwrap.json",
    "poetry.lock",
    "Pipfile.lock",
    "requirements.txt.lock",
    "Cargo.lock",
    "ext.config.ts",
    "tailwind.config.ts",
    "next.config.ts",
    "composer.lock",
    ".lock",
    ".env",
    ".env.*",
    "*.env",
    "*.cfg",
    "*.ini",
    ".flaskenv",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".github",
    ".gitlab-ci.yml",
    ".prettierrc",
    ".eslintrc",
    ".eslintignore",
    ".stylelintrc",
    ".editorconfig",
    ".jshintrc",
    ".pylintrc",
    ".flake8",
    "mypy.ini",
    "pyproject.toml",
    "tsconfig.json",
    "webpack.config.js",
    "babel.config.js",
    "rollup.config.js",
    "jest.config.js",
    "karma.conf.js",
    "vite.config.js",
    "next.config.js",
    "*.min.js",
    "*.min.css",
    "*.bundle.js",
    "*.bundle.css",
    "*.map",
    "*.gz",
    "*.zip",
    "*.tar",
    "*.tgz",
    "*.rar",
    "*.7z",
    "*.iso",
    "*.dmg",
    "*.img",
    "*.msix",
    "*.appx",
    "*.appxbundle",
    "*.xap",
    "*.ipa",
    "*.deb",
    "*.rpm",
    "*.msi",
    "*.exe",
    "*.dll",
    "*.so",
    "*.dylib",
    "*.o",
    "*.obj",
    "*.jar",
    "*.war",
    "*.ear",
    "*.jsm",
    "*.class",
    "*.pyc",
    "*.pyd",
    "*.pyo",
    "__pycache__",
    "*.a",
    "*.lib",
    "*.lo",
    "*.la",
    "*.slo",
    "*.dSYM",
    "*.egg",
    "*.egg-info",
    "*.dist-info",
    "*.eggs",
    "node_modules",
    "bower_components",
    "jspm_packages",
    "lib-cov",
    "coverage",
    "htmlcov",
    ".nyc_output",
    ".tox",
    "dist",
    "build",
    "bld",
    "out",
    "bin",
    "target",
    "packages/*/dist",
    "packages/*/build",
    ".output",
    "__init__.py",
    ".gitkeep",
}
IGNORED_EXTS = {
    ".log",
    ".tmp",
    ".bak",
    ".csv",
    ".tsv",
    ".swp",
    ".swo",
    ".old",
    ".orig",
    ".rej",
    ".pid",
    ".seed",
    ".dump",
    ".dat",
    ".db",
    ".db-journal",
    ".sqlite",
    ".sqlite3",
    ".lock",
    ".cache",
}

ALLOWED_FILE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".h",
    ".c",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".cs",
    ".kt",
    ".swift",
    ".m",
    ".vue",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".less",
    ".json",
    ".xml",
    ".yaml",
    ".yml",
    ".sh",
    ".bash",
    ".ps1",
    ".bat",
    ".sql",
}
DOC_FILE_EXTENSIONS = {".md", ".rst"}


MAIN_DIR = Path(__file__).resolve().parents[1]

LOG_DIR = MAIN_DIR / "logs"

# Repository configuration
DATA_DIR = MAIN_DIR / "data"
REPOS_DIR = DATA_DIR / "repo"
DOCS_DIR = DATA_DIR / "docs"
STRUCTURE_DIR = DATA_DIR / "struct"
VECTORS_DIR = DATA_DIR / "vectors"
