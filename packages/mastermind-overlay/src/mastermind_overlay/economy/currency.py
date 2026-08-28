CURRENCY_PER_TURN_LEFT: int = 2
CURRENCY_PER_MARGIN_LEFT: int = 5

def reward_for(turns_left: int, margin: int) -> int:
    return turns_left * CURRENCY_PER_TURN_LEFT + margin // CURRENCY_PER_MARGIN_LEFT
