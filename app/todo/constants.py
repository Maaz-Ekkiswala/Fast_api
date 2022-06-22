from enum import Enum


class TodoStatus(int, Enum):
    PENDING = 0
    IN_PROGRESS = 1
    DONE = 2
