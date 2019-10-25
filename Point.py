class Point:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

    def convert(self):
        return (self.x, self.y)

    def __lt__(self, other):
        return self.c < other.c

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash(repr(self))

    def __str__(self):
        return "(%d, %d)"% (self.x, self.y)
