import pygame
from Game import Game

from Piece import Piece
from Constants import PIECESIZE, GameState, COLORS


class GameWindow:
    def __init__(self, game: Game) -> None:
        pygame.init()
        pygame.font.init()
        pygame.font.get_init()

        self.height = game.getGameHeight() * PIECESIZE
        self.width = game.getGameWidth() * PIECESIZE + 200

        self.game = game

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris")
        pygame.display.set_icon(pygame.image.load("assets/Tetris_logo.webp"))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("freesanbold.ttf", 30)
        self.pauseFont = pygame.font.SysFont("freesanbold.ttf", 60)

        self.running = True
        self.tickSpeed = 60
        self.spedUp = False

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if (self.game.gameState == GameState.MENU):
                if event.type == pygame.KEYDOWN:
                    self.game.gameState = GameState.PLAYING

            if (self.game.gameState == GameState.PLAYING):
                self.control_game_movement(event)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.game.resetGame()
                    return
                elif event.key == pygame.K_p:
                    self.game.gameState = self.game.gameState.switch_pause()

        self.game.tick(
            self.tickSpeed if not self.spedUp else self.tickSpeed / 15)

        self.clock.tick(self.tickSpeed)

        self.render_game_field()

        self.render_display_text()

        pygame.display.update()

    def control_game_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.spedUp = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.game.move_left()
            elif event.key == pygame.K_RIGHT:
                self.game.move_right()
            elif event.key == pygame.K_DOWN:
                self.spedUp = False
            elif event.key == pygame.K_UP:
                self.game.playingPiece.rotate()
                self.game.checkRotation()

    def render_game_field(self) -> None:
        self.surface.fill(COLORS["background"])

        pygame.draw.rect(
            self.surface, COLORS["secondaryBackground"],
            pygame.Rect(self.width - 200, 0, 200, self.height)
        )

        for row in range(self.game.getGameHeight()):
            for col in range(self.game.getGameWidth()):
                if self.game.landedPieces[row][col] != None:
                    pygame.draw.rect(self.surface, self.game.landedPieces[row][col], pygame.Rect(
                        col * PIECESIZE, row *
                        PIECESIZE, PIECESIZE, PIECESIZE
                    ))
                    self.drawBorder(col * PIECESIZE,
                                    row * PIECESIZE, 3)

        if (self.game.playingPiece != None):
            self.drawPiece(self.game.playingPiece, 3)

        if (self.game.nextPiece != None):
            self.drawNextPiece()

    def render_display_text(self):
        if (self.game.gameState == GameState.PAUSED):
            self.renderText("Game paused", (50), self.height/2, self.pauseFont)

        if (self.game.gameState == GameState.GAME_OVER):
            self.renderText("Game over", (50), self.height/2, self.pauseFont)

        if (self.game.gameState == GameState.MENU):
            self.renderText("Press any button to play", (50),
                            self.height/2, self.pauseFont)

        self.renderText("Score: " + str(self.game.score),
                        self.width - 180, 30, self.font)

        self.renderText("Highscore: " + str(self.game.highscore),
                        self.width-180, 80, self.font)

    def renderText(self, text: str, x: int, y: int, font) -> None:
        img = font.render(text, True, COLORS["white"])
        rect = img.get_rect()
        rect.topleft = (x, y)
        self.surface.blit(img, rect)

    def drawPiece(self, piece: Piece, border_width: int) -> None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in piece.image():
                    x = piece.window_x + j * PIECESIZE
                    y = piece.window_y + i * PIECESIZE
                    pygame.draw.rect(self.surface, piece.color, pygame.Rect(
                        x, y,
                        PIECESIZE,
                        PIECESIZE
                    ))
                    self.drawBorder(x, y, border_width)

    def drawBorder(self, left: int, top: int, width: int) -> None:
        pygame.draw.rect(self.surface, COLORS["black"], pygame.Rect(
            left, top, PIECESIZE, width
        ))
        pygame.draw.rect(self.surface, COLORS["black"], pygame.Rect(
            left, top, width, PIECESIZE
        ))
        pygame.draw.rect(self.surface, COLORS["black"], pygame.Rect(
            left + PIECESIZE - width, top, width, PIECESIZE
        ))
        pygame.draw.rect(self.surface, COLORS["black"], pygame.Rect(
            left, top + PIECESIZE - width, PIECESIZE, width
        ))

    def drawNextPiece(self) -> None:
        pygame.draw.rect(self.surface, COLORS["black"], pygame.Rect(
            self.width - 180, self.height/2-100, 160, 200
        ))
        self.renderText("Next piece:", self.width - 160,
                        self.height/2 - 130, self.font)
        self.drawPiece(Piece(self.game.getGameWidth()+0.5, self.game.getGameHeight()/2-2,
                       self.game.nextPiece.color, self.game.nextPiece.type), 3)
