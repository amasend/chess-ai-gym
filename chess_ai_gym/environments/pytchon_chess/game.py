from chess.pgn import Game as BaseGame

__all__ = [
    "Game"
]


class Game(BaseGame):
    def __init__(self) -> None:
        super().__init__()
