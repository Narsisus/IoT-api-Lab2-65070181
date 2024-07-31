from unicodedata import category
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
# # from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    description = Column(String, index=True)
    summary = Column(String, index=True)
    is_published = Column(Boolean, index=True)
    categories = Column(ARRAY(String), index=True)

class Cafe(Base):
    __tablename__ = 'cafes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    comments = Column(String, index=True)

class order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    comments = Column(String, index=True)
    status = Column(String, index=True)
    cafe_id = Column(Integer, ForeignKey('cafes.id'))
