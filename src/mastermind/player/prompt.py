from mastermind.core.colors import Color


def guess() -> list[Color]:
    guess: list[Color] = []
    while len(guess) != 4:
        try:
            color_idx = int(input("Please enter color idx >> "))
            guess.append(Color(color_idx))
        except Exception as e:
            print(f"Error: player.guess : {e}")
    print(f"You choose {[c.name + "," for c in guess]}")
    return guess
