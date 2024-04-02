# Wordle

In this interview we'll write a simple version of the popular online word game,
Wordle.

If you're unfamiliar with this game, take a minute to try it out!
https://www.nytimes.com/games/wordle/index.html. We won't judge you if you don't
solve it—it can be tricky! Try starting with a guess like CRANE or SLICE.

Write a basic interface that allows you to play Wordle. It should have a way to
input guesses (e.g., a terminal input or HTML text box), should allow you to
guess six times (let's assume the guesses are real words), and for each guess
should print which letters were correct. Here are a few helpful emoji you can
use if you like: 🟩, 🟨, ⬜.

Let's first focus on the "happy path" of checking guesses against the answer. We
can come back to validation, error handling, and interface polish if we have
time!

## Worked example

Let's say the correct answer is EARTH:

```
CRANE
⬜🟨🟨⬜🟨
EERIE
🟩⬜🟩⬜⬜
ONION
⬜⬜⬜⬜⬜
WATER
⬜🟩🟨🟨🟨
EARTH
🟩🟩🟩🟩🟩
```

Or, if you prefer using letters instead of emoji:

```
CRANE
WYYWY

EERIE
GWGWW

ONION
WWWWW

WATER
WGYYY

EARTH
GGGGG
```
