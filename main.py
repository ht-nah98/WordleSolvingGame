import random
from termcolor import colored
import nltk
from nltk.corpus import words

class WordleAI:
    def __init__(self, word_list):
        self.word_list = word_list
        self.words_five = [word for word in self.word_list if len(word) == 5]

    def choose_random_word(self):
        return random.choice(self.words_five)

    def generate_ai_guess(self, feedback, previous_guesses):
        unused_letters = set('abcdefghijklmnopqrstuvwxyz')

        for letter, status in feedback.items():
            if status == 'exact':
                unused_letters.discard(letter)
            elif status == 'elsewhere':
                unused_letters.discard(letter)

        ai_guess = ''.join(random.choice(list(unused_letters)) for _ in range(5))
        return ai_guess

class WordleGame:
    def __init__(self):
        nltk.download('words')
        self.words_five = [word.lower() for word in words.words() if len(word) == 5]
        self.ai_player = WordleAI(self.words_five)

    def print_menu(self):
        print("Let's play Wordle:")
        print("Type a 5-letter word you guess:\n")

    def play_game(self, player_type):
        is_play = ""
        word = ""
        feedback = {}  # Initialize feedback dictionary
        previous_guesses = set()  # Initialize set to store previous guesses

        while is_play.lower() != "q":
            if player_type == 'user':
                word = self.get_user_guess()
            elif player_type == 'ai':
                word = self.ai_player.generate_ai_guess(feedback, previous_guesses)

            attempts_left = 6
            self.print_menu()

            while attempts_left > 0:
                guess = input().lower()[:5] if player_type == 'user' else word
                self.display_feedback(guess, word)
                if guess == word:
                    print(colored(f"Congratulations! You got the wordle in {6 - attempts_left + 1} attempts.", 'red'))
                    break

                attempts_left -= 1

            if attempts_left == 0:
                print(f"Incorrect, the wordle was ..{word}")

            is_play = input("Want to play again? Type q to exit, or anything else to play again.\n")

    def get_user_guess(self):
        return input().lower()[:5]

    def display_feedback(self, guess, word):
        for i in range(5):
            if guess[i] == word[i]:
                print(colored(guess[i], 'green'), end="")
            elif guess[i] in word:
                print(colored(guess[i], 'yellow'), end="")
            else:
                print(colored(guess[i], 'grey'), end="")
        print()

if __name__ == "__main__":
    wordle_game = WordleGame()
    player_type = input("Choose player type (user or ai): ").lower()
    wordle_game.play_game(player_type)
