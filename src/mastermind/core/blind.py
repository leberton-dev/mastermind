from enum import Enum


class Blind(Enum):
    SMALL = (1.0, "Small Blind", False)
    BIG = (1.5, "Big Blind", False)
    BOSS = (2.0, "Boss Blind", True)

    def __init__(self, multiplier: float, label: str, is_boss: bool) -> None:
        self.multiplier: float = multiplier
        self.label: str = label
        self.is_boss: bool = is_boss

