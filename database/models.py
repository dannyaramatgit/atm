from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

import database

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cash(Base):
    __tablename__ = "cash"

    id = Column(Integer, primary_key=True)
    val = Column(Float, unique=True)
    type = Column(String)
    amount = Column(Integer)
