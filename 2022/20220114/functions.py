import random
from collections import defaultdict, Counter


def preprocess(mystery_words):
    """
    Gather basic information around mystery words, such as:
    - most frequent chars
    - most frequent chars per position
    Return a set and a counter object
    """
    # use a counter to determine top 5 chars
    char_count = Counter()
    for word in mystery_words:
        for char in set(word):  # more helpful to limit to distinct chars
            char_count[char] += 1

    # Build set of these chars:
    top_chars = set([t[0] for t in char_count.most_common(6)])

    # Determine top chars per position for mystery words:
    pos_counter = [Counter() for _ in range(5)]
    for word in mystery_words:
        for i, c in enumerate(word):
            pos_counter[i][c] += 1

    return top_chars, pos_counter

def limit_guess(guess_list, pos_counter):
    """
    For eligible guess words determine which most closely
    match the most common positions (3 per index)

    Return dictionary of these letters / indices
    """
    position_dict = defaultdict(set)

    for word in guess_list:
        match = 0
        for i, c in enumerate(word):
            comm = [t[0] for t in pos_counter[i].most_common(3)]
            if c in comm:
                match += 1
        position_dict[match].add(word)

    return position_dict


# Functions for checking guess against mystery word
def excludeChars(guess, mystery_word):
    """Determine which chars should not be guessed again
       Return set of these chars
    """
    exclude_chars = set()
    for letter in guess:
        if letter not in mystery_word:
            exclude_chars.update(letter)
    return exclude_chars


def includeChars(guess, mystery_word):
    """Determine which chars should be guessed again
       Return set of these chars
    """
    include_chars = set()
    for letter in guess:
        if letter in mystery_word:
            include_chars.update(letter)
    return include_chars


def properPos(guess, mystery_word):
    """Determine if any chars properly guessed are in the proper index for the mystery word
        Return dict with index
    """
    pos_dict = defaultdict(set)
    for i, char in enumerate(guess):
        if char == mystery_word[i]:
            pos_dict[char].add(i)
    return pos_dict


def improperPos(guess, mystery_word):
    """Determine if any chars properly guessed are eligible but in the improper index for the mystery word
        Return dict with index
        
        Note: Minor bug - if a mystery word has 2 chars that are the same there could be issues in return
    """
    impos_dict = defaultdict(set)
    for i, char in enumerate(guess):
        if (char in mystery_word) and (char != mystery_word[i]):
            impos_dict[char].add(i)
    return impos_dict


# functions for search

def charRemoveWords(ex_set, in_set, guess_words):
    """Remove words from eligible guesses based on ex_set (excluded chars) and
       in_set (included chars). 
       
       Return new set
    """
    new_set = set()
    for guess in guess_words:
        # check if illicit chars are in guess, then remove
        ex_len = len([char for char in guess if char in ex_set])

        # check if we have eligible chars, if not remove
        in_len = len([char for char in guess if char in in_set])

        # ensure 0 ex_len and > 0 in_len
        if (ex_len == 0) and (in_len >= len(in_set)):
            new_set.add(guess)
        else:
            continue
    return new_set


def idxRemoveWords(proper_pos, improper_pos, guess_words):
    """Limit words from eligible guesses based on index information
    
        I think this will be the toughest....
        
        Nice thing with default is we can check for keys that don't exist 
       
       Return new set
    """
    new_set = set()

    # first we need to know all the correct indices found
    len_idx = 0
    for k, v in proper_pos.items():
        len_idx += len(v)

    for guess in guess_words:

        # track if a word has a bad_idx
        bad_idx = len([i for i, char in enumerate(guess) if i in improper_pos[char]])

        # track if a word has proper_idx 
        proper_idx = len([i for i, char in enumerate(guess) if i in proper_pos[char]])

        if (bad_idx > 0) or (proper_idx != len_idx):
            continue
        else:
            new_set.add(guess)
    return new_set


# Next function: Need to determine an optimal next guess
# All words are equal in terms of matching indices 
# - look for most frequent chars
# - look for most diversity -> how many unique chars outside of what is in inclusion list
def nextGuess(include_chars, guess_words):
    """Maximize diversity of characters"""
    max_dict = defaultdict(set)

    # iterate and find new chars from each guess
    for guess in guess_words:
        new_chars = len(set([c for c in guess]) - include_chars)
        max_dict[new_chars].add(guess)

    # find max
    max_idx = max(max_dict.keys())

    # rndomly choose from
    return random.choice(tuple(max_dict[max_idx]))


def nextGuessDistinct(include_chars, guess_words):
    """Maximize diversity of characters"""
    max_dict = defaultdict(set)

    # iterate and find new chars from each guess
    for guess in guess_words:
        new_chars = len(set([c for c in guess]) - include_chars)
        max_dict[new_chars].add(guess)

    # find max
    max_idx = max(max_dict.keys())

    # return set
    return max_dict[max_idx]


def nextGuessFrequent(include_chars, top_chars, guess_words):
    """Maximize number of frequent chars that are new"""
    max_dict = defaultdict(set)

    # iterate and find new chars from each guess
    for guess in guess_words:
        new_chars = set([c for c in guess]) - include_chars
        new_top = len([c for c in new_chars if c in top_chars])
        max_dict[new_top].add(guess)

    # find max
    max_idx = max(max_dict.keys())

    # return set
    return max_dict[max_idx]


def optimalPosChoice(pos_counter, guess_list, proper_pos):
    """
    Strategy for choosing next guess:
    - First determine what indices are already correct - we ignore
    - Next iterate over indices incorrectly matched for each possible guess word
    - If letter falls under a most common index from mystery analysis then +1
    - Store in defaultdict where key = match count, val = word

    Return max set of eligible words

    """
    best_dict = defaultdict(set)

    # get cur idx - we avoid these when searching
    cur_idx = []
    for k, v in proper_pos.items():
        if v != set():
            cur_idx.append(list(v)[0])

    # determine which guesses have most common features to pos_counter
    for word in guess_list:
        match = 0
        for i, c in enumerate(word):
            if i in cur_idx:
                pass
            # common for position
            comm = [t[0] for t in pos_counter[i].most_common(3)]
            if c in comm:
                match += 1

        # add word to set indexed by total matches
        best_dict[match].add(word)

    # find max
    try:
        max_idx = max(best_dict.keys())
        return best_dict[max_idx]
    except ValueError:
        return set() # return empty set

def optimalstrategy(guess, mystery_word, guess_list, mystery_list, pos_counter, guesses=3):
    """
    Single word process includes:
    - establishing params
    - general character set build:
        - chars not in word (wrong guesses)
        - chars in word
        - chars in word in wrong position
        - chars in word in correct position
    - apply information from above to whittle set down:
        - remove guess words that have any exclude chars or are missing any include chars
        - remove guess words that have improper indices
    - making a guess:
        - utilize filtered guest words
        - maximize words that a)
    - on last step need to intersect with mystery list (per Zach's twitter comment) to ensure a mystery
      word is being used as a guess

    Return 1 for a win and 0 for a loss
    """
    exclude_chars = set()  # words can't include these
    include_chars = set()  # words need to include these
    proper_pos = defaultdict(
        set)  # stores the proper indices for a letter
    improper_pos = defaultdict(
        set)  # stores the improper indices for a letter
    i = 0
    guess_words = guess_list.copy()
    #print(f"Mystery word: {mystery_word}")
    #print(f"Initial guess: {guess}")

    while i < guesses:
        if guess == mystery_word:
            return 1

        # remove guess from guess words
        guess_words.remove(guess)

        # not accepted:
        exclude_chars.update(excludeChars(guess, mystery_word))

        # accepted:
        include_chars.update(includeChars(guess, mystery_word))

        # proper pos
        temp_dict = properPos(guess, mystery_word)
        for k, v in temp_dict.items():
            proper_pos[k] = proper_pos[k].union(v)

        # improper pos
        temp_dict = improperPos(guess, mystery_word)
        for k, v in temp_dict.items():
            improper_pos[k] = improper_pos[k].union(v)

        # Debugger:
        #print(proper_pos)
        #print(improper_pos)
        #print(include_chars)
        #print(exclude_chars)

        # Move into reduce step
        # we first reduce our set of words down based on excluded & included chars
        new_words = charRemoveWords(exclude_chars, include_chars, guess_words)

        # we then reduce our set of words down based on proper & improper indices
        guess_words = idxRemoveWords(proper_pos, improper_pos, new_words)
        #print(guess_words)

        ### Determine next guess
        # optimal position strategy
        opt_guess = optimalPosChoice(pos_counter, guess_words, proper_pos)

        # determine guesses with most diversity -> guaranteed to have a result
        div_guesses = nextGuessDistinct(include_chars, guess_words)

        # see if we have overlap between div_guesses and top_guesses
        best_guesses = div_guesses.intersection(opt_guess)
        #print(f"Best guesses: {best_guesses}")

        # Zach on Twitter approved of this step
        if i == (guesses - 2):
            # last guess so needs to be a mystery word
            pick_set = guess_words.intersection(set(mystery_list))
            guess = random.choice(tuple(pick_set))
            #print(f"Last guess: {guess}")
            return guess == mystery_word
        elif len(best_guesses) > 0:
            guess = random.choice(tuple(best_guesses))
        else:
            guess = random.choice(tuple(div_guesses))

        #if i < guesses:
            #print(f"Next guess: {guess}")
        i += 1
    return 0