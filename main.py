"""
This is a version of Wordle written in Python.
- let's build a cli version first, then move on to the web version
"""

from collections import Counter
import random
from typing import Dict, List, Counter
from enum import Enum
from colorama import Fore, Back, Style


class GameStatus(Enum):
    WON = 1
    CONTINUE = 0
    LOST = -1


class Wordle:
    def __init__(self, wordlist: List[str], secret: str, allowed_guesses: int):
        if not bool(wordlist):
            raise ValueError("The word list must be a non-empty list")

        for word in wordlist:
            if not self._is_valid_word(word):
                raise ValueError(
                    f"Invalid word: [{word}]- All words in the word list must have a length of 5 and be made up of alphabetical letters"
                )

        if not self._is_valid_word(secret):
            raise ValueError(
                f"Invalid secret: [{secret}]- The secret word must have a length of 5 and be made up of alphabetical letters"
            )

        if allowed_guesses <= 0:
            raise ValueError(
                f"There must be minimum 1 number of guesses allowed to make the game playable"
            )

        self.wordlist: List[str] = wordlist
        self.secret: str = secret
        self.allowed_guesses: int = allowed_guesses

    def _is_valid_word(self, word: str) -> bool:
        # check if the word's length is 5 and all characters within word are alphabetical letters.
        return len(word) == 5 and all([ch.isalpha() for ch in word])

    def set_secret(self, secret: str) -> None:
        if secret not in self.wordlist:
            raise ValueError(
                f"secret must be a word within word list.\n word list = {self.wordlist}"
            )
        self.secret = secret

    def display_result(self, result: List[str], guessed: str) -> None:
        stringify_result: str = "".join(result)
        for i, ch in enumerate(guessed):
            ch_result: str = result[i]

            if ch_result == "G":  # GREEN- ch exists within secret at index i
                background = Back.GREEN
                foreground = Fore.WHITE
            if ch_result == "W":  # WHITE- ch doesn't exist within secret
                background = Back.WHITE
                foreground = Fore.BLACK
            elif ch_result == "Y":  # YELLOW- ch exists within secret but at the wrong position
                background = Back.YELLOW
                foreground = Fore.WHITE
            else:
                raise ValueError(f"Containing wrong color within result: {stringify_result}")

            print(foreground + background + ch, end="")
            print(Style.RESET_ALL, end=" ")

    def make_guess(self, guessed: str) -> GameStatus:
        """
        - if a character is at the correct position with the secret, make it green => guessed[i] == secret[i] => make it green
        - if a character completely doesn't exist within secret, make it white.
        - if a character exists within secret but at the wrong position (guessed[i] in secret but guessed[i] != secret[i]), make it yellow.

        - Can we use a character multiple times to mark yellow?
        - If a character already counted by a green and a yellow beforehand, we have to remove its count.
        => use character counts for secret.

        Let's say the correct answer is EARTH:

                 01234
        guessed: CRANE ['C', 'R', 'A', 'N', 'E']
        secret:  EARTH ['E', 'A', 'R', 'T', 'H']
        answer:  WYYWY ['W', 'Y', 'Y', 'W', 'Y']

                 C R A R E
                 E A R T H
                 W Y Y W Y

                 0 1 2 3 4
        guessed: E E R I E
        secret:  E A R T H   { E: 0, A: 1, R: 0, T: 1, H: 1 }
        answer:  G W G W W

                 0 1 2 3 4
        guessed: O N I O N
        secret:  E A R T H
        answer:  W W W W W

                 0 1 2 3 4
        guessed: W A T E R
        secret:  E A R T H { E: 1, A: 1, R: 1, T: 1, H: 1 }
        answer:  W G Y Y Y

                 0 1 2 3 4
        guessed: E A R T H
        secret:  E A R T H
        answer:  G G G G G

                 0 1 2 3 4
        guessed: T A S T E
        secret:  E A R T H
        answer:  W G W G Y

        - have an array called ans to return the result to the guessed word (a list of 'G', 'Y', and 'W'). ans = ['' for _ in range(5)]
        - have a dictionary call ch_freq to count the frequency of each character within secret: ch_freq:Dict[str, int] = Counter(secret)
        - loop thru the guessed list to identify all the greens: if secret[i] == guessed[i]:
            - mark ans[i] as 'G'.
            - decrement ch_freq[secret[i]] by 1.
        - loop thru the guessed list to identify the yellow and white:
            - if ans[i] is already marked as 'G' (green), skip: continue
            - otherwise, if ch_freq[guessed[i]] > 0:
                - mark ans[i] as 'Y'.
                - decrement ch_freq[guessed[i]] by 1
            - otherwise (ch_freq[guessed[i]] < 0):
                - mark ans[i] as 'W'
        """
        if not self._is_valid_word(guessed):
            raise ValueError(
                "Error: The guessed word must have a length of 5 and be made up of alphabetical letters"
            )

        if self.allowed_guesses <= 0:
            raise RuntimeError("Error: You've run out of available guesses.")

        ans: List[str] = ["" for _ in range(5)]
        ch_freq: Dict[str, int] = Counter(self.secret)
        # check green
        for i, ch in enumerate(guessed):
            if ch == self.secret[i]:
                ans[i] = "G"
                ch_freq[ch] -= 1

        # check white and yellow
        for i, ch in enumerate(guessed):
            if ans[i] == "G":
                continue

            if ch_freq[ch] > 0:
                ans[i] = "Y"
                ch_freq[ch] -= 1
            else:
                ans[i] = "W"

        # decrement self.allowed_guesses by 1
        self.allowed_guesses -= 1

        self.display_result(ans, guessed)
        print()

        if ans == ["G", "G", "G", "G", "G"]:
            return GameStatus.WON
        elif self.allowed_guesses <= 0:
            return GameStatus.LOST
        else:
            print(f"You have {self.allowed_guesses} remaining guesses")
            return GameStatus.CONTINUE


def main():
    wordlist: List[str] = [
        "APPLE",
        "BRAVE",
        "CHAIR",
        "CRANE",
        "CRAVE",
        "DREAM",
        "EARTH",
        "EERIE",
        "TASTE",
        "FLUTE",
        "GHOST",
        "HAPPY",
        "IDEAL",
        "JUICE",
        "KNOCK",
        "LIGHT",
        "MAGIC",
        "NIGHT",
        "OCEAN",
        "PRIZE",
        "QUIET",
        "RIVER",
        "SPACE",
        "TRAIN",
        "UNITY",
        "VALID",
        "WATER",
        "YOUTH",
    ]
    secret = random.choice(wordlist)
    wordle = Wordle(wordlist=wordlist, secret=secret, allowed_guesses=5)
    print("================================")
    print("Welcome to Wordle!")
    print("================================")
    while True:
        guessed: str = input("Enter a 5 letter word: ").upper()
        result: "GameStatus" = wordle.make_guess(guessed)

        if result == GameStatus.CONTINUE:
            continue
        elif result == GameStatus.WON:
            print(f"Congratulation! The secret word is [{secret}]. You've won")
        elif result == GameStatus.LOST:
            print(f"You've ran out of guesses. The secret word is [{secret}]")

        break


if __name__ == "__main__":
    main()
