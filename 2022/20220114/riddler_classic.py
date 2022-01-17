import pandas as pd
import random
from collections import defaultdict, Counter
from functions import excludeChars, includeChars, properPos, improperPos, charRemoveWords, idxRemoveWords, \
    nextGuessDistinct, nextGuessFrequent, preprocess, limit_guess, optimalPosChoice, optimalstrategy
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
final_guess = position_dict[4].union(position_dict[5])
print(f"Candidate starting guesses include {len(final_guess)} words")

# Limit mystery word validation to a subset until top words are found
sample_mystery = random.sample(mystery_list, int(round(0.3 * len(mystery_list),0)))
print(f"Validation mystery count is {len(sample_mystery)} words")

# Let's try some sample words:
guess = 'dreks'
mystery = 'dross'
print(f"Mystery word is: {mystery}")
optimalstrategy(guess = guess, mystery_word = mystery, guess_list = guess_list,
                mystery_list = mystery_list, pos_counter=pos_counter, guesses = 3)

# # Run on sample:
# start = time.time()
words_checked = 1
# # sample process:
# win_tracker = {}
win = 0
guess = 'crate'
for mystery_word in sample_mystery:
    win += optimalstrategy(guess=guess, mystery_word=mystery_word, guess_list=guess_list, mystery_list=mystery_list, pos_counter=pos_counter, guesses=4)
#
print(f"Win percent: {win/len(sample_mystery):.5f}")