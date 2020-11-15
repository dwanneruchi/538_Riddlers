"""Ran locally"""
import numpy as np
from numba import jit
import time
import statistics
import multiprocessing
import os
from scipy.stats import binom

# main process
def mp_process():

    # total core sims
    tot_core_sims = 3000000

    # File locations
    file_name = os.getpid()
    out_filename = "output/" + str(file_name) + ".txt"

    ### BUILD cdf dictionary for possible turns left, heads we need.
    tot_turns = 101
    max_heads = 51
    bin_cdf_dict = {}

    for n in range(tot_turns+1):
        for k in range(max_heads + 1):
            # using k-1 still .cdf func seems to be <= x
            bin_cdf_dict[k,n] = 1 - binom.cdf(k-1,n,0.5)
    
    # run simulations, pass in dict
    tot_games = 0
    super_loser = 0

    for j in range(tot_core_sims):
        
        exceeds, winner = faster_game(bin_cdf_dict)
        
        # out of loop
        if exceeds:
            tot_games += 1

            if winner == False:
                super_loser += 1
        
        if (j+1) % 1000000 == 0:
            print(f"Iteration {j+1}:")
            print(f"\tTotal games with > 0.99: {tot_games}")
            print(f"\tSuper loser games: {super_loser}")
            print(f"\tPercent: {100 * super_loser / tot_games:.2f}")
    
    # store in unique text based on PID
    with open(out_filename, 'a') as out_file:
        out_file.write(str(super_loser) + '\n')
        out_file.write(str(tot_games) + '\n')
        out_file.close()


def faster_game(bin_cdf):
    """Run simulations for 101 flips, relies on a pre-build CDF dict"""
    
    # General game params:
    heads = 0
    winning_flips = 51
    tot_flips = 101
    flips = 0
    exceeds = False
    winner = False

    # Run 101 flips. If a clear winner arises, end game
    for _ in range(tot_flips):

        # flip coin once
        coin = np.random.binomial(1,0.5)

        # update heads count, flips, and tails 
        heads += coin
        flips += 1
        tails = flips - heads   

        # needed to win:
        needed_heads = winning_flips - heads
        turns_left = tot_flips - flips
        
        # check if game is over for either person
        if heads >= winning_flips:
            winner = True
        
        ### Solve for likelihood of getting needed_heads or more based on remaining turns
        k = needed_heads # whats the likelihood of getting up to needed heads but not over; 
        n = turns_left

        if k >= 0:
            # binom.cdf calculates P(X <= k)
            p = bin_cdf.get((k,n))
            if p >= 0.99:
                exceeds = True
            
    return exceeds, winner

if __name__ == '__main__':
    """
       Will run simulations across 4 cores
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

    # start processes
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # wait for everything to finish
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    print("All done")
    end = time.time()
    print(f"Total time: {end - start}")