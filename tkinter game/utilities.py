# import packages
from random import *

# random function that produces more high #s than low #s (linear) 
# primarily to spread out enemy shooting
def linear_random(limit):
    r1 = random()
    r2 = random()
    
    hack = 0
    while hack < 1000:
        if r1 > r2:
            return r1

        r1 = random()
        r2 = random()
        
        hack += 1

    return 0
    