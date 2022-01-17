import pandas as pd
import random
from functions import preprocess, limit_guess, optimalstrategy, optimalstrategyTest
import time
import pickle

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

# Limit to the top matches -> helps speed things up
final_guess = position_dict[4].union(position_dict[5])
print(f"Candidate starting guesses include {len(final_guess)} words")

# Limit mystery word validation to a subset until top words are found
sample_mystery = random.sample(mystery_list, int(round(0.15 * len(mystery_list),0)))
print(f"Validation mystery count is {len(sample_mystery)} words")

# # Run on sample:
start = time.time()

# # sample process:
win_tracker = {}
words_checked = 1
for guess in final_guess:
    win = 0
    if words_checked % 25 == 0:
        print(f"Checked a total of {words_checked} words")
        print(f"Total time so far: {time.time() - start:.3f}")
        top_word = max(win_tracker, key=win_tracker.get)
        win_p = win_tracker[top_word] / len(sample_mystery)
        print(f"Max win prob so far is: {win_p:.5f} with top word {top_word}")

    for mystery_word in sample_mystery:
        win += optimalstrategyTest(guess=guess, mystery_word=mystery_word, guess_list=guess_list, mystery_list=mystery_list, pos_counter=pos_counter, guesses=3)
    win_tracker[guess] = win

    words_checked += 1

top_word = max(win_tracker, key=win_tracker.get)
win_p = win_tracker[top_word] / len(sample_mystery)
print(f"Top win prob on sample was: {win_p:.5f} with top word {top_word}")

# get top 10 words from sample run - will iterate through all words for these to find final winner
start = time.time()
top_word_list = [x[0] for x in sorted(win_tracker.items(), key=lambda x: x[1], reverse=True)[:10]]
print(f"Reviewing peformance for {len(top_word_list)} words")

with open('top_ten.pkl', 'wb') as f:
    pickle.dump(top_word_list, f)

win_tracker = {}
for guess in top_word_list:
    win = 0
    for mystery_word in mystery_list:
        win += optimalstrategyTest(guess=guess, mystery_word=mystery_word, guess_list=guess_list, mystery_list=mystery_list, pos_counter=pos_counter, guesses=3)
    win_tracker[guess] = win

print(f"Total time: {time.time() - start:.3f}")
top_word = max(win_tracker, key=win_tracker.get)
win_p = win_tracker[top_word] / len(mystery_list)
print(f"Win prob is: {win_p:.5f} with top word {top_word}")