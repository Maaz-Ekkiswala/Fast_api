from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column

from db.base import Base


class User(Base):
    __tablename__ = 'user'

    username = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)

    user_for_todo = relationship("ToDo", back_populates="user_todo")
