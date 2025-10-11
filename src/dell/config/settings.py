from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DELL",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,  # Carrega .env automaticamente
)

# Configuração do Rich Logging baseada no ambiente
LOGGING_CONFIG = {
    "rich_enabled": settings.get("rich_logging", True),
    "environment": "development" if settings.debug else "production",
    "console_output": settings.get("console_logging", True),
    "file_output": settings.get("file_logging", True),
}

# Uso no código:
# settings.DATABASE_PASSWORD  # Vem do .env ou .secrets.toml
# settings.POSTGRES_USER      # Vem do .env
