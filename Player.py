import enum

class direction(enum.Enum):
    RIGHT = "Right"
    LEFT = "Left"
    UP = "Up"
    DOWN = "Down"


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = direction.RIGHT
