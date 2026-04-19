import uuid
from sqlalchemy import Column, String, Float, Integer, JSON, Text
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String)
    brand = Column(String)
    price = Column(Float)
    rating = Column(Float)
    review_count = Column(Integer)
    description = Column(Text)
    features = Column(JSON) # Store list of strings
    image_url = Column(String)
    image_description = Column(Text) # To store Gemini output
    embedding = Column(JSON, nullable=True) # Optional back-up of the vector

    def __repr__(self):
        return f"<Product(title={self.title}, price={self.price})>"
