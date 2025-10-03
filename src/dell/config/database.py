from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dell.config.settings import settings

# URL de conexão usando as configurações
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.database_host}:{settings.database_port}/{settings.POSTGRES_DB}"

# Engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
