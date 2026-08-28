from enum import Enum


class RoundTier(Enum):
    STANDARD = (1.0, "Standard", False)
    HARDENED = (1.5, "Hardened", False)
    FINAL = (2.0, "Final", True)

    def __init__(self, multiplier: float, label: str, is_final: bool) -> None:
        self.multiplier: float = multiplier
        self.label: str = label
        self.is_final: bool = is_final
