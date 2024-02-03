import enum
import collections

class Tip(enum.Enum):
    ABSENT = 0
    PRESENT = 1
    CORRECT = 2

def score(secret, guess):
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
print(score("hello", "heloe"))

def filter_words(words, guess, score):
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

print(filter_words(["abe", "ace"], "ark", score("a??", "ark")))
print(filter_words(["abe", "ace"], "abi", score("a??", "abi")))
print(filter_words(["aazz"], "xxaa", score("azzz", "xxaa")))
print(filter_words(["azzz", "zazz", "zzaz", "zzza"], "xxaa", score("azzz", "xxaa")))