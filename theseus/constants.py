from enum import auto, Enum

class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

globals().update(Direction.__members__)