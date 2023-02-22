from enum import Enum


class Type(str, Enum):
    TASK = "task"
    BUG = "bug"
    STORY = "story"


class Priority(str, Enum):
    HIGH = "high"
    HIGHEST = "highest"
    MEDIUM = 'medium'
    LOW = "low"
    LOWEST = "lowest"


class Status(str, Enum):
    PENDING = "pending"
    MOVE_TO_DEVELOPMENT = "move_to_development"
    IN_PROGRESS = "in_progress"
    DONE = "done"
