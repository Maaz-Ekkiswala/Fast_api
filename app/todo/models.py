from sqlalchemy import Integer, Text, Boolean, String, ForeignKey, Enum
from sqlalchemy.sql.schema import Column

from app.todo.constants import TodoStatus
from db.base import Base


class ToDo(Base):
    __tablename__ = 'todo'

    title = Column(String, nullable=False)



class TODoItems(Base):
    __tablename__ = 'todo_items'

    title = Column(String, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id", ondelete="CASCADE"))
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatus))
