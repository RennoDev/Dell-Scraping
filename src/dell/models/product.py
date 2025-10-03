from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from dell.models.base import Base


class Product(Base):
    __tablename__ = "products"

    model = Column(String(255), nullable=False)  # "Dell XPS 13"
    price = Column(Numeric(10, 2))  # 1299.99
    link = Column(String(500))  # URL do produto
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
