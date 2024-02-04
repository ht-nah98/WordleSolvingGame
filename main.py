import requests
import random
import string
import enum
import collections
from termcolor import colored

class Tip(enum.Enum):
    ABSENT = 0  # word not in secret word
    PRESENT = 1  # word in secret word but wrong position
    CORRECT = 2  # word in secret word and correct position

class WordleGame:
    def __init__(self, word_length=5):
        self.WORD_LENGTH = word_length
        self.ALLOWABLE_CHARACTERS = set(string.ascii_lowercase)
        self.WORDS = set()

    def download_word_list(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            self.WORDS = {
                word.lower()
                for word in response.text.splitlines()
                if len(word) == self.WORD_LENGTH and set(word) <= self.ALLOWABLE_CHARACTERS
            }
        else:
            print(f"Failed to download the word list from {url}.")
            self.WORDS = set()

    def display_feedback(self, guess, word):
        for i in range(self.WORD_LENGTH):
            if guess[i] == word[i]:
                print(colored(guess[i], 'green'), end="")
            elif guess[i] in word:
                print(colored(guess[i], 'yellow'), end="")
            else:
                print(colored(guess[i], 'grey'), end="")
        print()

    def get_secret_word(self):
        print("Write your secret word:")
        secret = input(">>> ")
        return secret.lower()

    # def score(self, secret, guess):
    #     # All characters that are not correct go into the usable pool.
    #     pool = collections.Counter(s for s, g in zip(secret, guess) if s != g)
    #     # Create a first tentative score by comparing char by char.
    #     score = []
    #     for secret_char, guess_char in zip(secret, guess):
    #         if secret_char == guess_char:
    #             score.append(Tip.CORRECT)
    #         elif guess_char in secret and pool[guess_char] > 0:
    #             score.append(Tip.PRESENT)
    #             pool[guess_char] -= 1
    #         else:
    #             score.append(Tip.ABSENT)

    #     return score

    # dont remove the duplicate letter if this letter is correct 
    def score(self, secret, guess):
        score = []
        for secret_char, guess_char in zip(secret, guess):
            if secret_char == guess_char:
                score.append(Tip.CORRECT)
            elif guess_char in secret:
                score.append(Tip.PRESENT)
            else:
                score.append(Tip.ABSENT)

        return score    

    # Method to filter words based on the guess and score
    def filter_words(self, words, guess, score):
        # Initialize an empty list to store the filtered words
        new_words = []
        # Iterate through each word in the current word pool
        for word in words:
            # only word have not CORRECT will appear on pool
            pool = collections.Counter(c for c, sc in zip(word, score) if sc != Tip.CORRECT)

            for char_w, char_g, sc in zip(word, guess, score):
                # Check conditions based on the score type
                if sc == Tip.CORRECT and char_w != char_g:
                    # Break if the character is correct but in the wrong position 
                    break
                elif char_w == char_g and sc != Tip.CORRECT:
                    # Break if the character is present but in the wrong position
                    break
                elif sc == Tip.PRESENT:
                    # Break if the character is present in the wrong position and the pool is empty
                    if not pool[char_g]:
                        break
                    pool[char_g] -= 1
                elif sc == Tip.ABSENT and pool[char_g]:
                    # Break if the character is absent but present in the pool
                    break
            else:
                # If the loop completes without breaking, the word passes all conditions
                new_words.append(word)

        # Return the list of filtered words
        return new_words


    def play_game(self):
        self.download_word_list("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")

        secret = self.get_secret_word()
        words = [word for word in self.WORDS if len(word) == len(secret)]
        print(len(words))
        attempts = 1

        while len(words) > 1 and attempts < 7:
            print(f"I'll guess randomly from my pool of {len(words)} words (Attempt {attempts}/6)...")
            sample = ", ".join(words[:8])
            end = ", among others..." if len(words) > 8 else "."
            print(f"I'm considering {sample}{end}")

            guess = random.choice(words)
            print(f"Hmmm, I'll guess {guess!r}...")
            self.display_feedback(guess, secret)
            sc = self.score(secret, guess)
            print(f"\tMy guess scored {sc}...")
            words = self.filter_words(words, guess, sc)
            attempts += 1
            print()
            print("print words: ", words)
            if len(words) == 1:
                break  # Exit the loop if only one word remains

        if not words or all(score == Tip.CORRECT for score in self.score(secret, words[0])):
            print(f"Congratulations! I guessed the word {secret!r} in {attempts} attempts.")
        else:
            print(f"Sorry, I couldn't guess the word. The correct word is {words[0]!r}.")




if __name__ == "__main__":
    game = WordleGame()
    game.play_game()
