import random
from collections import defaultdict

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
    
def improperPos(guess, mystery_word, pos_dict):
    """Determine if any chars properly guessed are eligible but in the improper index for the mystery word
        Return dict with index
        
        Note: Minor bug - if a mystery word has 2 chars that are the same there could be issues in return
    """
    impos_dict = defaultdict(set)
    for i, char in enumerate(guess):
        if (char in mystery_word) and (char != mystery_word[i]) and (i not in pos_dict[char]):
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
            
        # check if we have any eligible chars, if not remove
        in_len = len([char for char in guess if char in in_set])
        
        # ensure 0 ex_len and > 0 in_len
        if (ex_len > 0):
            continue
        elif (in_len < len(in_set)):
            continue
        else:
            new_set.add(guess)  
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
    for k,v in proper_pos.items():
        len_idx += len(v)
    
    for guess in guess_words: 
        
        # track if a word has a bad_idx
        bad_idx = len([i for i,char in enumerate(guess) if i in improper_pos[char]])
        
        # track if a word has proper_idx 
        proper_idx = len([i for i,char in enumerate(guess) if i in proper_pos[char]])
        
        if (bad_idx > 0) or (proper_idx != len_idx):
            continue
        else:
            new_set.add(guess)
    return new_set

# Next function: Need to determine an optimal next guess
# All words are equal in terms of matching indices 
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