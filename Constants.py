from enum import Enum

PIECESIZE: int = 40

HIGHSCORE_FILE_PATH: str = ""

COLORS: dict[str, tuple[int, int, int]] = {
    "background": (66, 73, 72),
    "black": (0, 0, 0),
    "secondaryBackground": (36, 40, 40),
    "white": (255, 255, 255)
}

PIECE_COLORS: dict[str, tuple[int, int, int]] = {
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "pink": (255, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255)
}

# 0  1  2  3
# 4  5  6  7
# 8  9 10 11
# 12 13 14 15

SHAPES: list[tuple[int, int, int, int]] = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]


class GameState(Enum):
    PLAYING = 0
    PAUSED = 1
    GAME_OVER = 2
    MENU = 3

    def switch_pause(self):
        if self.value == 0:
            return GameState.PAUSED
        elif self.value == 1:
            return GameState.PLAYING
