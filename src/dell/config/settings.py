from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DELL",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,  # Carrega .env automaticamente
)

# Uso no código:
# settings.DATABASE_PASSWORD  # Vem do .env ou .secrets.toml
# settings.POSTGRES_USER      # Vem do .env
