"""
This is a version of Wordle written in Python.
- let's build a cli version first, then move on to the web version
"""

from typing import List
from enum import Enum


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

    def make_guess(self, guessed: str) -> int:
        """
        Some examples:

        """
