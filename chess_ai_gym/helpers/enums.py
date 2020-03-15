from enum import Enum

__all__ = [
    "SideType"
]


class SideType(Enum):
    """Enum indicates which turn it is."""
    WHITE = True
    BLACK = False
