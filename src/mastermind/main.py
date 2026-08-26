import mastermind.bot as bot
import mastermind.player as player

from mastermind.core.colors import Color

_MAX_TURNS = 10


def play():
    secret_code: list[Color] = bot.secret.random_code()

    for _ in range(_MAX_TURNS):
        guess = player.prompt.guess()
        result = bot.score.feedback(secret_code, guess)
        print(f"Result is : {result}")
        if result == (4, 0):
            print("You won.")
            break
    print("You lost.")


def main():
    playing = True

    while playing:
        play()
        if input("Do you want to play again ? (y/N) >> ").lower() == "n":
            playing = False


if __name__ == "__main__":
    main()
