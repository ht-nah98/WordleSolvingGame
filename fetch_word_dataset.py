import requests
import string

ALLOWABLE_CHARACTERS = set(string.ascii_letters)
ALLOWED_ATTEMPTS = 10
WORD_LENGTH = 5

def fetch_words_from_github():
    github_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

    try:
        # Fetch the content of words_alpha.txt from the GitHub repository
        response = requests.get(github_url)
        response.raise_for_status()  # Raise an exception for bad responses (e.g., 404 Not Found)

        # Split the content into a list of words
        words_list = response.text.splitlines()

        # Filter words to include only those with 5 letters and composed of allowable characters
        words_list = [
            word.lower() for word in words_list 
            if len(word) == WORD_LENGTH and set(word) <= ALLOWABLE_CHARACTERS
        ]

        return words_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching words from GitHub: {e}")
        return None

# Example usage:
WORDS = fetch_words_from_github()

if WORDS is not None:
    print(f"Total words fetched: {len(WORDS)}")
    # You can now use the WORDS list in your program
else:
    print("Failed to fetch words from GitHub.")