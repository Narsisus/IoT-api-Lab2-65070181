from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
# from sqlalchemy.orm import relationship

from database import Base

class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    id_number = Column(String, unique=True, index=True)
    birth_date = Column(Date, index=True)
    gender = Column(String, index=True)
