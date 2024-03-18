from random import randint
import re
import numpy as np
import random
from Tree import Calc
calculate = Calc.evaluate

def rand(value):
        return randint(1, value)

def roll_dice(dice_string: str) -> tuple:
    # Parse the input string to get the number of dice and the number of sides on each dice
    dice_part = re.split(r'd|D', dice_string)
    
    if dice_part[0] == '':
        dice_part[0] = '1'

    num_dice = int(dice_part[0])
    num_sides = int(dice_part[1])
    #print(dice_part)
    
    if(num_sides > 100):
        raise Exception("The Number of sides must not be more than 100")
    if(num_dice > 100):
        raise Exception("We don't have that many dice")
    

    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    return rolls, sum(rolls)


def getRolls(expression):
    x = re.split('[+]|[*]|[-]|[/]|\s', expression)
    rolls = []
    finder = re.compile('[1-9]*[0-9]*(d|D)[1-9][0-9]*')
    for i in range(0, len(x)):
        if(finder.match(x[i])): 
            rolls.append(re.search(finder,x[i]).group())
    return rolls

def rollAll(expression):
    rollsexpr = getRolls(expression)
    total = 0
    rolling = []
    for i in range(0,len(rollsexpr)):
        try:
            rolls, result = roll_dice(rollsexpr[i])
        except Exception as e:
            raise Exception(e)
        rolling.append(rolls)
    return rolling, total

def sumOfArray(array): 
    total = 0
    for i in range(0, len(array)):
        total += array[i]
    return total

def initialScoreRoll(): 
    rolls = []
    new = []
    removed_list = []
    total = []


    for j in range(0, 6):
        new = []
        for i in range(0, 4):
            d6 = rand(6)
            new.append(d6)
        new.sort()
        removed = new.pop(0)
        removed_list.append(removed)
        total.append(sumOfArray(new))
        rolls.append(new)
    
    #Now format the String
    end_expr = "Rolls:{},{},{},{},{},{}\nRemoved:{}\nTotal:{}".format(rolls[0], rolls[1], rolls[2], rolls[3], rolls[4], rolls[5], removed_list, total);

    return end_expr

def process_args(expr):
    #Recebe uma lista de argumentos que serão rolls de dados como xDn 
    print("Something")
    
def format_roll(expr):
    rolls = re.split(r'([+\-*\/])', expr)
    results_string = ""
    message_to_user = expr + " = "
    for part in rolls:
        if part.strip():
            if part.isdigit():  # If it's a constant number
                results_string += f"{part} "
                message_to_user += f"{part} "
            elif 'd' in part or 'D' in part:  # If it's a dice roll
                roll_results, _ = roll_dice(part)
                results_string += f"({' + '.join(map(str, roll_results))}) "
                message_to_user += f"{part}({' '.join(map(str, roll_results))}) "           
            else:  # If it's an operator
                results_string += part + " "
                message_to_user += part + " "

    result = calculate(results_string.strip())
    message_to_user += f"= :star: {result} :star:"
    
    return results_string.strip(), message_to_user.strip()


