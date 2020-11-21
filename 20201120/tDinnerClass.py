import numpy as np
from collections import defaultdict

# Class for simulating the passing of cranberries for a single Thanksgiving dinner 
class TDinner():
    def __init__(self, num_people):
        self.curr = 0 # we start off
        self.people_list = [x for x in range(num_people)]
        self.tracker = defaultdict(lambda: 0) # as we add keys, we just keep track of counts
        self.tracker[0] += 1 # person starting has touched this 
        self.last_person = 99999 # outrageous value so we know this is not our answer
       
    def fullFeed(self):
        """Work around the table until everyone has access to cranberry sauce"""
        continueCircle = True
       
        while continueCircle:
           
            # do a pass
            self.__passOnce()
           
            # check if we can stop
            continueCircle = self.__allTouch()

        loser = self.last_person
       
        return loser
       
    def __passOnce(self):
        """ Look at self.curr & randomly choose index to pass to next"""
        if np.random.choice(2, 1)[0] == 0:
            next_move = self.people_list[(self.curr - 1)]
        else:
            # need to handle scenario where we are on element n of list len n and + 1 (should go to 0th person)
            max_solv = lambda x : x + 1 if (x < len(self.people_list) - 1) else 0
            next_move = max_solv(self.curr)
           
        # add next_move idx to tracker & add 1
        self.tracker[next_move] += 1
       
        # update curr
        self.curr = next_move
           
    def __allTouch(self):
        """Determine if everyone has experienced Cranberry Sauce"""
        missing_list = [x for x in self.people_list if x not in self.tracker.keys()]
       
        # if we dip below 2 then we only have 1 person left
        if len(missing_list) < 2:
            self.last_person = missing_list[0]
            return False
        return True

if __name__ == "__main__": 
    test = TDinner(10)
    loser = test.fullFeed()
    print(f"Our loser was {loser}")