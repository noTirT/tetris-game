from Constants import HIGHSCORE_FILE_PATH


class FileUtil:
    @staticmethod
    def save_highscore(highscore: int) -> None:
        with open(HIGHSCORE_FILE_PATH + "highscore.txt", "w") as f:
            f.write(str(highscore))

    @staticmethod
    def get_highscore() -> int:
        with open(HIGHSCORE_FILE_PATH + "highscore.txt", "r") as f:
            line = f.read()
            if (line == ""):
                return 0
            return int(line)
