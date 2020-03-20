from typing import TYPE_CHECKING, Union, List, Optional

if TYPE_CHECKING:
    from uuid import UUID

__all__ = [
    "NoMoreMoves",
    "NodesNotPopulated"
]


class CustomError(Exception):
    def __init__(self, message: str, errors: List[str]) -> None:
        super().__init__(message)
        self.errors = errors


class NoMoreMoves(CustomError):
    def __init__(self, leaf_id: Union['UUID', int], errors: Optional[List[str]] = None) -> None:
        super().__init__(f"No more moves to explore in a leaf: {leaf_id}", errors)


class NodesNotPopulated(CustomError):
    def __init__(self, leaf_id: Union['UUID', int], errors: Optional[List[str]] = None) -> None:
        super().__init__(f"Nodes are not populated for leaf: {leaf_id}", errors)
