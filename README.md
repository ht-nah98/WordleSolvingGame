# Wordle Solving Game

Welcome to the Wordle Solving Game, where algorithms help the computer find hidden words within 6 attempts.

## Project Files

### 1. word_guess_api_solve.py
   - Uses the guess word API to retrieve data.
   - Handles the guessing process using the API.

### 2. word_daily_api_solve.py
   - Uses the daily word API to retrieve data.
   - Implements the game logic for daily words.

### 3. check_filter_score_f.py
   - Manages special cases in word filtering and scoring.
   - Helps handle various scenarios during the guessing process.

### 4. data_to_score_test.py
   - A utility script to check and convert data responses from the API to the game's own score type.

## How to Play

1. **Download Word List:**
   - The game downloads a word list from [URL] during initialization.

2. **Generate First Guess:**
   - A random word is generated as the initial guess to start the game.

3. **Guessing Process:**
   - The game makes sequential guesses based on feedback from the API.
   - The feedback is converted into a custom score type for further processing.

4. **Filtering and Scoring:**
   - The game uses various algorithms to filter the word list based on the feedback received.
   - Special cases are handled using `check_filter_score_f.py`.

5. **Winning or Losing:**
   - The game announces whether it successfully guessed the word within 6 attempts or not.

## Running the Game

1. Clone the repository:

   ```bash
   git clone [repository_url]
   cd WordleSolvingGame
