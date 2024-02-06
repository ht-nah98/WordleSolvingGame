import string
from pathlib import Path
from collections import Counter
from itertools import chain
import operator
import httpx
import asyncio
import requests
import string
from fetch_word_dataset import fetch_words_from_github
# ALLOWABLE_CHARACTERS = set(string.ascii_letters)
# ALLOWED_ATTEMPTS = 10
# WORD_LENGTH = 5

# def fetch_words_from_github():
#     github_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

#     try:
#         # Fetch the content of words_alpha.txt from the GitHub repository
#         response = requests.get(github_url)
#         response.raise_for_status()  # Raise an exception for bad responses (e.g., 404 Not Found)

#         # Split the content into a list of words
#         words_list = response.text.splitlines()

#         # Filter words to include only those with 5 letters and composed of allowable characters
#         words_list = [
#             word.lower() for word in words_list 
#             if len(word) == WORD_LENGTH and set(word) <= ALLOWABLE_CHARACTERS
#         ]

#         return words_list

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching words from GitHub: {e}")
#         return None

class WordleSolver:
    def __init__(self, words_list, allowable_characters, allowed_attempts, word_length):
        self.ALLOWABLE_CHARACTERS = allowable_characters
        self.ALLOWED_ATTEMPTS = allowed_attempts
        self.WORD_LENGTH = word_length
        self.WORDS = self.filter_words(words_list)

    def filter_words(self, words_list):
        return {
            word.lower()
            for word in words_list
            if len(word) == self.WORD_LENGTH and set(word) <= self.ALLOWABLE_CHARACTERS
        }

    def calculate_word_commonality(self, word, letter_frequency):
        score = 0.0
        for char in word:
            score += letter_frequency[char]
        return score / (self.WORD_LENGTH - len(set(word)) + 1)

    def sort_by_word_commonality(self, words, letter_frequency):
        sort_by = operator.itemgetter(1)
        return sorted(
            [(word, self.calculate_word_commonality(word, letter_frequency)) for word in words],
            key=sort_by,
            reverse=True,
        )

    def display_word_table(self, word_commonalities):
        for (word, freq) in word_commonalities:
            print(f"{word:<10} | {freq:<5.2}")

    async def fetch_daily_word(self, guess):
        url = "https://wordle.votee.dev:8000/daily"
        params = {
            "guess": guess,
            "size": 5
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                result_str = "".join(["G" if result['result'] == 'correct' else "Y" if result['result'] == 'present' else "?" for result in data])
                return result_str
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None

    async def computer_guess_from_api(self, word_vector, possible_words, letter_frequency):
        """
        Method to perform computer guessing using an API.

        Args:
            word_vector (list): The current word vector representing the possible characters for each position.
            possible_words (set): Set of possible words based on the current state of the game.
            letter_frequency (dict): Frequency of letters in the English language.

        Returns:
            None
        """
        for attempt in range(1, self.ALLOWED_ATTEMPTS + 1):
            print(f"\nAttempt {attempt} with {len(possible_words)} possible words")
            
            # Display the top 15 words based on word commonality
            display_words = self.sort_by_word_commonality(possible_words, letter_frequency)[:15]
            self.display_word_table(display_words)

            # The computer selects the first word in the possible words set as its guess
            computer_guess = list(possible_words)[0]
            print(f"Computer's guess: {computer_guess}")

            # Send the computer's guess to the API and receive the response
            response = await self.fetch_daily_word(computer_guess)
            print(f"Response from API: {response}")

            # Update the word vector and possible words based on the API response
            for idx, letter in enumerate(response):
                # if letter is G, remain in the word_vector only for this letter 
                # example from [['a,b,c,d,e,f']...] - > [['a'],....]
                if letter == "G":
                    word_vector[idx] = {computer_guess[idx]}
                
                # if letter Y, remove this letter at this index in vector_word and keep other letter remain
                elif letter == "Y":
                    try:
                        word_vector[idx].remove(computer_guess[idx])
                    except KeyError:
                        pass
                
                # if letter is ?, remove this letter in all vector_word
                elif letter == "?":
                    for vector in word_vector:
                        try:
                            vector.remove(computer_guess[idx])
                        except KeyError:
                            pass

            # Narrow down the possible words based on the API response
            possible_words = self.match(word_vector, possible_words)

            # Check if the computer guessed the secret word correctly
            if "G" * self.WORD_LENGTH == response:
                print(f"\nComputer guessed the secret word: {computer_guess}")
                break
        else:
            print(f"\nComputer couldn't guess the secret word.")

    def match(self, word_vector, possible_words):
        matching_words = []
        for word in possible_words:
            if self.match_word_vector(word, word_vector):
                matching_words.append(word)
        return matching_words

    def match_word_vector(self, word, word_vector):
        assert len(word) == len(word_vector)
        for letter, v_letter in zip(word, word_vector):
            if letter not in v_letter:
                return False
        return True

    async def main(self):
        letter_counter = Counter(chain.from_iterable(self.WORDS))
        letter_frequency = {
            character: value / letter_counter.total()
            for character, value in letter_counter.items()
        }

        possible_words = self.WORDS.copy()
        word_vector = [set(string.ascii_lowercase) for _ in range(self.WORD_LENGTH)]

        await self.computer_guess_from_api(word_vector, possible_words, letter_frequency)

if __name__ == "__main__":
    github_words = fetch_words_from_github()

    if github_words is not None:
        solver = WordleSolver(github_words, set(string.ascii_letters), 10, 5)
        asyncio.run(solver.main())
    else:
        print("Failed to fetch words from GitHub.")
