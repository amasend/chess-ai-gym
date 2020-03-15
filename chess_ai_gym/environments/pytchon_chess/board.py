from chess import Board as BaseBoard

__all__ = [
    "Board"
]


class Board(BaseBoard):
    def __init__(self, starting_position: str) -> None:
        super().__init__(fen=starting_position)
