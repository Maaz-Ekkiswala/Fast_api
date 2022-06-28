from sqlalchemy import Integer, Text, Boolean, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column

from app.todo.constants import TodoStatus
from db.base import Base


class ToDo(Base):
    __tablename__ = 'todo'

    title = Column(String, nullable=False)

    todo_items = relationship("ToDoItems", back_populates="todo")


class ToDoItems(Base):
    __tablename__ = 'todo_items'

    title = Column(String, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id", ondelete="CASCADE"))
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatus))

    todo = relationship("ToDo", back_populates="todo_items")


class User(Base):
    __tablename__ = 'user'

    username = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
