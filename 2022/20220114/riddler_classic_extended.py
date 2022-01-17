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

### Read in words from 15% sample
with open('top_ten.pkl', 'rb') as f:
    top_word_list = pickle.load(f)

for guess_count in [4,5,6]:
    print(f"Performance for {guess_count} guesses")
    start = time.time()
    win_tracker = {}
    for guess in top_word_list:
        win = 0
        for mystery_word in mystery_list:
            win += optimalstrategyTest(guess=guess, mystery_word=mystery_word, guess_list=guess_list, mystery_list=mystery_list, pos_counter=pos_counter, guesses=guess_count)
        win_tracker[guess] = win

    print(f"Total time: {time.time() - start:.3f}")
    top_word = max(win_tracker, key=win_tracker.get)
    win_p = win_tracker[top_word] / len(mystery_list)
    print(f"Win prob is: {win_p:.5f} with top word {top_word}")