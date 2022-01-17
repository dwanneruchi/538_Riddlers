### Brief Overview

Nothing impressive here, the best solution I saw was able to achieve around a 60% success rate in 3 guesses which is amazing (link: https://laurentlessard.com/bookproofs/optimal-wordle/)! The function I ended up using also has a `debug` parameter which lets me review the general process. My approach works well (the set of possible guesses get really small!) but not nearly as well as the dynamic programming solution shared in the earlier link.

### Approach
- I start by reducing starter words to a candidate list of approximately 300 from the eligible guess list. 
  - These are determined by first determining which character-index pairs are most frequent in the mystery words.
  - I then find which guess words best match at each position, which is how I whittle my list down. 
- I use brute force to determine which starter words lead to most success. It should be noted that I did not write this with any seeds set, therefore my approach is not deterministic. That should be improved!
  - I first iterate through a random sample of 20% of mystery words to determine top performing starter words. 
  - Then I try a subset of the top starter words across all mystery words to determine my top. 
- General process for making a guess:
  - Initial starter word
  - Pass through some filtering:
    - Determine which chars need to exist - use to reduce guess word set
    - Determine which chars do not next in word - use to reduce guess word set
    - Determine which matched chars are in wrong position - use to reduce guess word set
    - Determine which matched chars are in proper position - use to reduce guess word set
  - For the second guess I build a few random "next guess sets", this is where my weakness really lies - my approach does not have a clear strategy!
    - optimalPosChoice: Find which set of guess words most matches the most frequent char-pos values determined above for indices not determined. Goal is to remove less likely pos-char but this is flawed in how 
    - div_guesses: Returns set of guess words that yields most diverse characters. The idea here being to make more guesses of distinct chars to better filter in next step.
    - I find the intersection between these sets (if it exists), hoping to capture a frequent char-pos that also maximizes new knowledge for next step
  - Filters listed above are applied again, helping to really reduce eligible guess set down. 
  - Final guess is a bit different:
    - At this point we should have a pretty small set of eligible guess words. The author of the Riddler shared via Twitter that we need to produce a guess word that is in the mystery word set, so I do an intersection of my remaining eligible guess set with the mystery words, and randomly choose a final guess.

### Success Rate for 3 guesses or less
- Sample pass on 15:
  - `prost` was able to correctly determine the word 38.0% of the time in <= 3 steps.
- Sample pass on 20%: 
  - `orant` was able to correctly determine the mystery word 39.1% of the time in <= 3 steps.
- Top performance over all mystery words:
  - `saint` was able to correctly determine the mystery word `35.9%` of the time in <= 3 steps.

### Success Rate for 4, 5 and 6 guesses: Top performance
