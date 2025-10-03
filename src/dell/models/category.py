from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from dell.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    products = relationship("Product", back_populates="category")
