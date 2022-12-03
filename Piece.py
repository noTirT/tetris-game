from Constants import PIECESIZE, SHAPES


class Piece:
    def __init__(self, x: int, y: int, color: tuple[int, int, int], type: int) -> None:
        self.window_x = x * PIECESIZE
        self.game_x = x
        self.window_y = y * PIECESIZE
        self.game_y = y

        self.rotation = 0
        self.color = color
        self.type = type

    def set_x(self, x: int) -> None:
        self.window_x = x * PIECESIZE
        self.game_x = x

    def set_y(self, y: int) -> None:
        self.window_y = y * PIECESIZE
        self.game_y = y

    def image(self) -> list[int]:
        return SHAPES[self.type][self.rotation]

    def rotate(self) -> None:
        self.rotation = (
            self.rotation+1) % len(SHAPES[self.type])

    def leftBorder(self) -> int:
        for i in range(4):
            col = []
            for j in range(4):
                col.append(j * 4 + i)
            for c in self.image():
                if c in col:
                    return i

    def rightBorder(self) -> int:
        for i in range(3, -1, -1):
            col = []
            for j in range(3, -1, -1):
                col.append(j * 4 + i)
            for c in self.image():
                if c in col:
                    return i

    def bottomBorder(self) -> int:
        for i in range(3, -1, -1):
            row = []
            for j in range(4):
                row.append(i * 4 + j)
            for c in self.image():
                if c in row:
                    return i
