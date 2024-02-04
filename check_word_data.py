# Specify the path to your word.txt file
file_path = './words_data/words.txt'

# Initialize a variable to count the number of words
word_count = 0

# Open the file and count the 5-character words
with open(file_path, 'r') as file:
    for line in file:
        # Split each line into words using whitespace as the separator
        words = line.split()
        
        # Filter the words with 5 characters and increment the count
        word_count += sum(1 for word in words if len(word) == 5)

# Print the total number of 5-character words
print("Number of 5-character words in the file:", word_count)
