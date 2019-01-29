from enum import Enum


class Actions(Enum):
    Configuration = 1
    Movement = 2
    Reset = 3


class BaseMessage:
    def __init__(self, action, obj):
        self.Action = action
        self.Object = obj
