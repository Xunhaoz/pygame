class Pos:
    def __init__(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]

    def to_index(self) -> None:
        self.x = (self.x - 175) // 50
        self.y = (self.y - 60) // 50

    def is_in_range(self, x: int, y: int, size: int) -> bool:
        return x <= self.x <= x + size and y <= self.y <= y + size


class Block:
    def __init__(self, number: int, pos: Pos, writable: bool):
        self.number = number
        self.pos = pos
        self.writable = writable
        self.valid = True
