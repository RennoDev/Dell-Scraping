# src/dell/main.py (novo)
from dell.config.rich_logging import setup_rich_logging
from dell.config.settings import LOGGING_CONFIG


def configure_app():
    """Configuração inicial da aplicação."""

    # Configurar logging bonito
    if LOGGING_CONFIG["rich_enabled"]:
        setup_rich_logging(
            environment=LOGGING_CONFIG["environment"],
            console_output=LOGGING_CONFIG["console_output"],
            file_output=LOGGING_CONFIG["file_output"],
        )


def main():
    configure_app()  # ← Configurar ANTES de usar qualquer logger

    # Agora todos os loggers ficam bonitos automaticamente!
    import logging

    logger = logging.getLogger(__name__)

    logger.info("Aplicação Dell Scraper iniciada! 🚀")
    logger.debug("Rich logging configurado")


if __name__ == "__main__":
    main()
