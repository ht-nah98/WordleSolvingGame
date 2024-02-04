import httpx
import enum
import collections
import random
from termcolor import colored

class Tip(enum.Enum):
    ABSENT = 0  # word not in secret word
    PRESENT = 1  # word in secret word but wrong position
    CORRECT = 2  # word in secret word and correct position

class WordleGame:
    def __init__(self, word_length=5):
        self.WORD_LENGTH = word_length
        self.ALLOWABLE_CHARACTERS = set("abcdefghijklmnopqrstuvwxyz")
        self.WORDS = set()

    def download_word_list(self, url):
        response = httpx.get(url)
        if response.status_code == 200:
            self.WORDS = {
                word.lower()
                for word in response.text.splitlines()
                if len(word) == self.WORD_LENGTH and set(word) <= self.ALLOWABLE_CHARACTERS
            }
        else:
            print(f"Failed to download the word list from {url}.")
            self.WORDS = set()

    async def fetch_random_word(self, guess):
        url = "https://wordle.votee.dev:8000/daily"
        params = {
            "guess": guess,
            "size": self.WORD_LENGTH,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                tip_feedback = [Tip.CORRECT if item['result'].upper() == 'CORRECT' else
                                Tip.PRESENT if item['result'].upper() == 'PRESENT' else
                                Tip.ABSENT for item in data]

                print("Result:", tip_feedback)
                return tip_feedback
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None

    def display_feedback(self, guess, tip_feedback):
        for i, (tip, char) in enumerate(zip(tip_feedback, guess)):
            if tip == Tip.CORRECT:
                print(colored(char, 'green'), end="")
            elif tip == Tip.PRESENT:
                print(colored(char, 'yellow'), end="")
            else:
                print(colored(char, 'grey'), end="")
        print()

    def score(self, secret, guess):
        pool = collections.Counter(s for s, g in zip(secret, guess) if s != g)
        correct_positions = set()

        score = []
        for i, (secret_char, guess_char) in enumerate(zip(secret, guess)):
            if secret_char == guess_char and i not in correct_positions:
                score.append(Tip.CORRECT)
                correct_positions.add(i)
            elif guess_char in secret and pool[guess_char] > 0:
                score.append(Tip.PRESENT)
                pool[guess_char] -= 1
            else:
                score.append(Tip.ABSENT)

        return score     

    def filter_words(self, words, guess, score):
        new_words = []
        for word in words:
            pool = collections.Counter(c for c, sc in zip(word, score) if sc != Tip.CORRECT)

            for char_w, char_g, sc in zip(word, guess, score):
                if sc == Tip.CORRECT and char_w != char_g:
                    break
                elif sc == Tip.PRESENT:
                    if char_g != char_w and not pool[char_g]:
                        break
                    pool[char_g] -= 1
                elif sc == Tip.ABSENT and pool[char_g]:
                    break
            else:
                new_words.append(word)

        return new_words

    async def play_game(self):
        self.download_word_list("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")

        words = [word for word in self.WORDS if len(word) == self.WORD_LENGTH]
        attempts = 1

        while len(words) > 1 and attempts < 7:
            print(f"I'll guess randomly from my pool of {len(words)} words (Attempt {attempts}/6)...")
            sample = ", ".join(words[:8])
            end = ", among others..." if len(words) > 8 else "."
            print(f"I'm considering {sample}{end}")

            guess = random.choice(words)
            print(f"Hmmm, I'll guess {guess!r}...")
            sc = await self.fetch_random_word(guess)
            self.display_feedback(guess, sc)
            words = self.filter_words(words, guess, sc)
            attempts += 1
            print()
            print("print words:", words)
        final_guess = words[-1] if words else guess
        final_result = await self.fetch_random_word(final_guess)
        self.display_feedback(final_guess, final_result)
        if final_result == [Tip.CORRECT] * self.WORD_LENGTH:
            print(f"Congratulations! I guessed the word {final_guess!r} in {attempts} attempts.")
        else:
            print("Can find the secret key")

if __name__ == "__main__":
    import asyncio
    game = WordleGame()
    asyncio.run(game.play_game())
