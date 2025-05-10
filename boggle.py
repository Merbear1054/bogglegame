"""Boggle game logic."""

from random import choice
import string

class Boggle:
    def __init__(self):
        self.words = self.read_dict("words.txt")

    def read_dict(self, dict_path):
        """Read dictionary file and return list of valid words."""
        with open(dict_path) as dict_file:
            return [w.strip().lower() for w in dict_file]

    def make_board(self):
        """Create and return a 5x5 board of random uppercase letters."""
        return [
            [choice(string.ascii_uppercase) for _ in range(5)]
            for _ in range(5)
        ]

    def check_valid_word(self, board, word):
        """Check if a word is valid dictionary word and can be found on the board."""
        word = word.lower()
        if word not in self.words:
            return "not-word"
        elif not self.find(board, word.upper()):
            return "not-on-board"
        else:
            return "ok"

    def find(self, board, word):
        """Check if the word can be constructed from the board."""
        for y in range(5):
            for x in range(5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True
        return False

    def find_from(self, board, word, y, x, seen):
        """Recursive search starting at y,x for the word."""
        if x < 0 or x >= 5 or y < 0 or y >= 5:
            return False
        if (y, x) in seen:
            return False
        if board[y][x] != word[0]:
            return False
        if len(word) == 1:
            return True

        seen = seen | {(y, x)}  # new set to avoid global mutation

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy != 0 or dx != 0:
                    if self.find_from(board, word[1:], y + dy, x + dx, seen):
                        return True

        return False

