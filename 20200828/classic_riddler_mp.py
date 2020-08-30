"""Ran in GCP"""
import numpy as np
from numba import jit
import time
import statistics
import multiprocessing
import os

# main process
def mp_process():

    n = 100
    file_name = os.getpid()
    out_filename = "output/" + str(file_name) + ".txt"
    total_games = [] # empty list to store results

    for i in range(n):
        deck = np.tile(np.arange(13),4) # build 52 total integers of 0-12; initial deck
        outcome = 0
        iterations = 0

        while outcome != 1:
            outcome = war_game_simple(deck) # output if winner in 26 or not
            iterations += 1

        total_games.append(iterations)

        # store in unique text based on PID
        with open(out_filename, 'a') as out_file:
             out_file.write(str(iterations) + '\n')
        out_file.close()

        if i % 25 == 0:
            print(f'You are on step {i}')

    mean_games = statistics.mean(total_games) # mean over n runs
    print(f'Mean games for n = {n} was {mean_games}')
    print(f'Total games played = {sum(total_games)}')

@jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def war_game_simple(deck): # Function is compiled to machine code when called the first time
    """ General Logic:
    - The game rules don't matter, really just need to build out a sequence of 13 that repeats 4x
    - Then shuffle the array each game
    - "deal" (subset array; each player gets 26 elements)
    - subtract arrays using element-wise comparison:
       - np.sum(p1 > p2): this counts the number of times p1 array element > p2 array element
       - Big note: Intentionally limited this to only one player since it was noted that
                   the granddaughter played until winning.
                   My answer would be 1/2 of this if either side could win.

    """
    np.random.shuffle(deck) # shuffle
    p1 = deck[:26]
    p2 = deck[26:]

    # find array of differences
    diff = np.sum(p1 > p2)

    # check logic of all elements - either must all be positive or negative
    if (diff == 26):
        return 1
    else:
        return 0

if __name__ == '__main__':
    """
       Will run 100 simulations across 10 cores

       For 1000 total simulations
       Note: Need this & not multithreading due to GIL in Python
       GIL = Global Interpreter Lock
    """
    # track total time
    start = time.time()

    # multiprocessing component
    p1 = multiprocessing.Process(target=mp_process)
    p2 = multiprocessing.Process(target=mp_process)
    p3 = multiprocessing.Process(target=mp_process)
    p4 = multiprocessing.Process(target=mp_process)
    p5 = multiprocessing.Process(target=mp_process)
    p6 = multiprocessing.Process(target=mp_process)
    p7 = multiprocessing.Process(target=mp_process)
    p8 = multiprocessing.Process(target=mp_process)
    p9 = multiprocessing.Process(target=mp_process)
    p10 = multiprocessing.Process(target=mp_process)

    # start processes
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()

    # wait for everything to finish
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()

    print("All done")
    end = time.time()
    print("Total time: {end - start}")