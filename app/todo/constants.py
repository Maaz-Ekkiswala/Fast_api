from enum import Enum


class TodoStatus(int, Enum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3
