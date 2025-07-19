import logging
from conf.config import LOG_DIR


class FileLoggerConfigurator:
    """Manager for handling log files."""

    def __init__(self):
        self.log_dir = LOG_DIR
        self.ensure_log_directory()

    def ensure_log_directory(self):
        """Create the log directory if it does not exist."""
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def clean_log_file(self, name: str):
        """Empty the content of a specific log file."""
        log_file_path = self.log_dir / f"{name}.log"
        if log_file_path.exists():
            with open(log_file_path, "w", encoding="utf-8"):
                pass

    def setup_logger(self, name: str, level: int = 0):
        """Set up a logger with the specified name and level."""

        const_logs_level = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]

        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            self.clean_log_file(name)  # Function invoke during develop
            # Set the default logging level
            logger.setLevel(const_logs_level[level])

            # Create file handler
            file_handler = logging.FileHandler(self.log_dir / f"{name}.log")
            file_handler.setLevel(const_logs_level[level])

            # Create formatter and add it to the handler
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            # Add the handler to the logger
            logger.addHandler(file_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(const_logs_level[level])
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        else:
            # If the logger already has handlers, just set the level
            logger.setLevel(const_logs_level[level])
            for handler in logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.setLevel(const_logs_level[level])

        return logger
