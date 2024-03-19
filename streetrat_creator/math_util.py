import numpy
import math


# You have Hit Points equal to 10 + (5[BODY and WILL averaged, rounding up]).
def calculate_hp(body, will):
    res = 10 + 5 * math.ceil((body + will)/2)
    return res

def calculate_humanity(emp):
    return emp * 10

def readjust_empathy_from_humanity(humanity):
    return humanity % 10 

if __name__ == "__main__":
    #You can check if the math is correct for HP in page 79 of CPR:Core Rulebook
    for i in range(2, 11): 
        for j in range(2, 16):
            print(calculate_hp(j, i), end=' ')
        print()