from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, func
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_date: datetime = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_date: datetime = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    created_by: int = Column(Integer)
    updated_by: int = Column(Integer)
