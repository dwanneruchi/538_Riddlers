import pandas as pd
from collections import defaultdict


def indexStatus(idx: str, guess: str, actual: str) -> str:
    """
    Return status representing the following relative to actual mystery word:
    - '0': char not in word
    - '1': char in word but not in proper position
    - '2': char in proper pos
    """
    # see if we have a clean match
    if guess[idx] == actual[idx]:
        return '2'

    # if not, check if char even exists
    for idx2, char in enumerate(actual):
        if (idx != idx2) and (guess[idx] == char):
            return '1'
    return '0'


def readInputs(folder: str) -> tuple[set, set]:
    """
    Read in eligible guess and mystery words
    """
    # read in mystery words
    mystery_corpus = pd.read_csv(folder + "mystery_words.csv", header=None)
    mystery_set = set([w[0] for w in mystery_corpus.values])

    # read in eligible guess words
    guess_corpus = pd.read_csv(folder + "guess_words.csv", header=None)
    guess_set = set([w[0] for w in guess_corpus.values])

    return mystery_set, guess_set

def buildEligibleMystery(feedback: str, mystery_set: set, guess: str = 'trace') -> list[str]:
    """
    Determine subsets of words that align with input feedback;
    Assume first guess is TRACE
    """
    subset_mystery = []
    for mystery in mystery_set:
        fb = ''
        for idx, char in enumerate(guess):
            fb = fb + indexStatus(idx, guess, mystery)
        if fb == feedback:
            subset_mystery.append(mystery)
    return subset_mystery

def findOptimalSecond(guess_set: set[str], sub_mystery_set: set[str], guess: str = 'trace') -> str:
    """

    """
    # build a dictionary which can store eligible guesses based on key
    step_two_remains = defaultdict(list)
    for mystery in guess_set:
        key = ''
        for idx, char in enumerate(guess):
            key = key + indexStatus(idx, guess, mystery)
        step_two_remains[key].append(mystery)

    # Determine total `n` for each guess from guess set
    # Comparison is across the remaining mystery set based on initial feedback
    n_count_dict = {}
    for guess in guess_set:
        distinct_keys = set()
        for mystery in sub_mystery_set:
            key = ''
            for idx, char in enumerate(guess):
                key = key + indexStatus(idx, guess, mystery)
            distinct_keys.add(key)

        # add len of set back to dict
        n_count_dict[guess] = len(distinct_keys)

    # get top guess, print stats:
    top_guess = max(n_count_dict, key=n_count_dict.get)
    print(f"top guess of {top_guess} should win {100 * n_count_dict[top_guess] / len(sub_mystery_set):.2f}% of the time")
    return top_guess


if __name__ == '__main__':

    mystery_set, guess_set = readInputs("../data/")
    print(f"You have {len(mystery_set)} mystery words and {len(guess_set)} words!")

    # Determined here: https://github.com/dwanneruchi/538_Riddlers/blob/master/2022/20220114/rc_strategy.ipynb
    guess = input("Recommended first guess is 'TRACE' - input guess now: ")

    # Prompt User for State of Wordle After Guess
    feedback = input("Input coding from initial guess: ")

    # Reduce to Possible Mystery Words
    eligible_mystery = buildEligibleMystery(feedback, mystery_set, guess)

    # Determine Optimal Guess Across Eligible Mystery Words:
    optimal_second = findOptimalSecond(guess_set, eligible_mystery, guess)

    # Prompt User for State of Wordle After Guess
    guess2 = input(f"Recommended second guess is {optimal_second} - input guess now: ")
    feedback2 = input("Input coding from second guess: ")

    # Reduce to Possible Mystery Words From Second Feedback
    eligible_mystery2 = buildEligibleMystery(feedback2, mystery_set, guess2)

    # Determine intersection
    final_guess_set = set(eligible_mystery).intersection(set(eligible_mystery2))

    print(f"Remaining options: {final_guess_set}")