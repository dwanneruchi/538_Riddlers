"""Ran locally on 4 core machine"""
import multiprocessing
import os
import pickle
import time
from tDinnerClass import TDinner
from collections import OrderedDict

# main process
def mp_process(fam_members = 20, sims = 250000):
    """Main process to run, accept number of family members and total simulations per core"""

    # Establish Params
    tot_core_sims = sims
    keys = [x for x in range(fam_members)]
    items = [(key, 0) for key in keys] # adding a default value of 0 for ordered dict
    loser_tracker = OrderedDict(items)

    # File locations: Saving as pickle 
    file_name = os.getpid()
    out_filename = str(file_name) + ".pickle"

    # Run sims
    for _ in range(sims):
        
        # new dinner class & run a single full feed process
        dinner = TDinner(fam_members)
        loser = dinner.fullFeed()
        
        # update dict 
        loser_tracker[loser] += 1
        
    # Pickle Sims
    with open(out_filename,'wb') as fout:
        pickle.dump(loser_tracker, fout)

if __name__ == '__main__':
    """
       Will run simulations across 4 cores
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