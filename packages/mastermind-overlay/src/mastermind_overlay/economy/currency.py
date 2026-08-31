CURRENCY_BASE_REWARD: int = 2
CURRENCY_PER_MARGIN: int = 15
MAX_MARGIN_REWARD: int = 3

def reward_for(turns_left: int, margin: int) -> int:
    reward = CURRENCY_BASE_REWARD

    if turns_left >= 1:
        reward += 1
    if turns_left >= 3:
        reward += 1
    if turns_left >= 5:
        reward += 1

    if margin >= 10:
        reward += 1
    if margin >= 30:
        reward += 1

    return reward
