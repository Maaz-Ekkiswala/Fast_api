from sqlalchemy import Integer, Text, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column

from app.todo.constants import TodoStatus
from db.base import Base


class ToDo(Base):
    __tablename__ = 'todo'

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)

    todo_items = relationship("ToDoItems", back_populates="todo")
    user_todo = relationship("User", back_populates="user_for_todo")


class ToDoItems(Base):
    __tablename__ = 'todo_items'

    title = Column(String, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id", ondelete="CASCADE"))
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatus))

    todo = relationship("ToDo", back_populates="todo_items")


