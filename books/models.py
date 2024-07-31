from unicodedata import category
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy.orm import relationship

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


