from typing import Union
import random

import math
from FileUtil import FileUtil

from Piece import Piece
from Constants import GameState, PIECE_COLORS, SHAPES


class Game:
    def __init__(self, height: int, width: int) -> None:
        self.playingPiece: Union[Piece, None] = None
        self.nextPiece: Union[Piece, None] = None
        self.landedPieces: list[list[tuple[int, int, int]]] = [
            [None for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width
        self.ticks = 0
        self.score = 0
        self.gameState: GameState = GameState.MENU
        self.highscore = FileUtil.get_highscore()

    def tick(self, tick_speed: int) -> None:
        if (self.gameState != GameState.PLAYING):
            return

        if self.nextPiece == None:
            self.chooseNextPiece()

        # Spawn new Piece if current one has landed
        if (self.playingPiece == None):
            self.spawnNewPiece()

        # Move current Piece down or unselect it if it has landed
        if (not self.intersects()):
            if self.ticks >= tick_speed:
                self.playingPiece.set_y(self.playingPiece.game_y+1)
                self.ticks = 0
            else:
                self.ticks += 1
        else:
            for p in self.playingPiece.image():
                offset_x = p % 4
                offset_y = math.floor(p / 4)
                self.landedPieces[self.playingPiece.game_y +
                                  offset_y][self.playingPiece.game_x + offset_x] = self.playingPiece.color
            self.spawnNewPiece()
        # remove row if it is full
        temp_score = 0
        for index, row in enumerate(self.landedPieces):
            if all(piece != None for piece in row):
                temp_score += 1
                self.clearRow(index)

        self.score += temp_score*temp_score

    def resetGame(self) -> None:
        self.landedPieces = [
            [None for _ in range(self.width)] for _ in range(self.height)]
        self.playingPiece = None
        self.nextPiece = None
        self.ticks = 0
        self.score = 0
        self.gameState = GameState.MENU

    def intersects(self) -> bool:
        if self.playingPiece.game_y + self.playingPiece.bottomBorder() + 1 >= self.height:
            return True
        for p in self.playingPiece.image():
            offset_x = p % 4
            offset_y = math.floor(p / 4)
            if self.landedPieces[self.playingPiece.game_y + offset_y + 1][self.playingPiece.game_x + offset_x] != None:
                if (self.playingPiece.game_y <= 0):
                    self.gameState = GameState.GAME_OVER
                    if self.score > FileUtil.get_highscore():
                        FileUtil.save_highscore(self.score)
                        self.highscore = self.score
                    self.resetGame()
                    return False
                return True
        return False

    def clearRow(self, row_number: int) -> None:
        for row_index in range(row_number, 0, -1):
            if all(piece == None for piece in self.landedPieces[row_index]):
                break

            if row_index == 0:
                self.landedPieces[0] = []
                break

            self.landedPieces[row_index] = []
            for piece in self.landedPieces[row_index-1]:
                if (piece == None):
                    self.landedPieces[row_index].append(None)
                else:
                    self.landedPieces[row_index].append(piece)

    def chooseNextPiece(self) -> None:
        self.nextPiece = Piece(self.width + 1, math.floor(self.height/2),
                               random.choice(list(PIECE_COLORS.values())), random.randint(0, len(SHAPES)-1))

    def spawnNewPiece(self) -> None:
        self.playingPiece = Piece(math.floor(
            self.width / 2)-2, 0, self.nextPiece.color, self.nextPiece.type)
        self.chooseNextPiece()

    def getGameHeight(self) -> int:
        return self.height

    def getGameWidth(self) -> int:
        return self.width

    def move_left(self) -> None:
        if self.playingPiece.game_x + self.playingPiece.leftBorder() <= 0:
            return

        for p in self.playingPiece.image():
            offset_x = p % 4
            offset_y = math.floor(p / 4)

            if self.landedPieces[self.playingPiece.game_y + offset_y][self.playingPiece.game_x + offset_x - 1] != None:
                return

        self.playingPiece.set_x(
            self.playingPiece.game_x - 1)

    def move_right(self) -> None:
        if (self.playingPiece.game_x + self.playingPiece.rightBorder() >= self.width - 1):
            return
        for p in self.playingPiece.image():
            offset_x = p % 4
            offset_y = math.floor(p / 4)

            if self.landedPieces[self.playingPiece.game_y + offset_y][self.playingPiece.game_x + offset_x + 1] != None:
                return

        self.playingPiece.set_x(
            self.playingPiece.game_x + 1)

    def checkRotation(self) -> None:
        while True:
            if self.playingPiece.game_x + self.playingPiece.leftBorder() < 0:
                self.playingPiece.set_x(self.playingPiece.game_x + 1)
            elif self.playingPiece.game_x + self.playingPiece.rightBorder() >= self.getGameWidth():
                self.playingPiece.set_x(self.playingPiece.game_x - 1)
            else:
                return
