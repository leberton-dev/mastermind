from dataclasses import dataclass

from mastermind_overlay.run.round_tier import RoundTier


@dataclass(frozen=True)
class RoundStarted:
    tier: RoundTier
