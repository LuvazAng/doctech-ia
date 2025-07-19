"""This script sets up a logger for the application using the FileLoggerConfigurator."""

from src.orchestrator import Orchestrator
from src.utils.loggers import FileLoggerConfigurator
from conf.config import GITHUB_TOKEN  # GITHUB_TOKEN no se usa directamente aquí


def main():
    """Main function to set up the logger."""
    logger_configurator = FileLoggerConfigurator()
    logger = logger_configurator.setup_logger(
        "application", level=0
    )  # Asume que level=0 es INFO o DEBUG
    logger.info("Logger has been set up successfully.")

    try:
        orchestrator_flow = Orchestrator(logger)
        orchestrator_flow.proccessing_repo(
            "https://github.com/LuvazAng/chatbot-llm.git", GITHUB_TOKEN
        )
    except IOError as e:
        logger.exception("An error occurred while running the application. %s", e)
    except (
        Exception
    ) as e:  # Captura cualquier otra excepción no manejada específicamente
        logger.exception(
            "An unexpected error occurred during the main execution: %s", e
        )


if __name__ == "__main__":
    main()
