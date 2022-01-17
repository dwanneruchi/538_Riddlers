import pandas as pd
import random
from functions import preprocess, limit_guess, optimalstrategyTest
import time

# read in mystery words
mystery_corpus = pd.read_csv("data/mystery_words.csv", header=None)
mystery_list = [w[0] for w in mystery_corpus.values]
mystery_words = set(mystery_list)

# read in eligible guess words
guess_corpus = pd.read_csv("data/guess_words.csv", header=None)
guess_list = [w[0] for w in guess_corpus.values]

# gather most freq chars and chars by position for mystery words
top_chars, pos_counter = preprocess(mystery_words)

# Determine guess words with most overlapping pos_counter - limits search space
position_dict = limit_guess(guess_list, pos_counter)

for i in range(6):
    try:
        print(f"Total position matches of {i} had {len(position_dict[i])}")
    except KeyError:
        continue

# Limit to the top matches
final_guess = position_dict[3].union(position_dict[4].union(position_dict[5]))
print(f"Candidate starting guesses include {len(final_guess)} words")

print(f"Is trace here: {'trace' in final_guess}")

# Limit mystery word validation to a subset until top words are found
sample_mystery = random.sample(mystery_list, int(round(0.2 * len(mystery_list),0)))
print(f"Validation mystery count is {len(sample_mystery)} words")




# Let's try some sample words:
guess = 'trace'
mystery = 'cacao'
#print(f"Mystery word is: {mystery}")
optimalstrategyTest(guess = guess, mystery_word = mystery, guess_list = guess_list,
                mystery_list = mystery_list, pos_counter=pos_counter, guesses = 3, debug = False)