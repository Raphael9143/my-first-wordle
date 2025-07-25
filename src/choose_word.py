import random

with open("assets/data/wordle_dict.txt", "r") as f:
    WORDLE_WORDS = [line.strip().upper() for line in f]

def choose_word():
    return random.choice(WORDLE_WORDS)

