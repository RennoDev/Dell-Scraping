from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True  # Não cria tabela para esta classe

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)  # Soft delete

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
