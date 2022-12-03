from Game import Game
from GameWindow import GameWindow


if __name__ == "__main__":
    # start program
    game = Game(20, 10)
    gameWindow = GameWindow(game)
    while gameWindow.running:
        gameWindow.tick()
