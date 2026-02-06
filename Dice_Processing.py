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
    x = re.split('[+]|[*]|[-]|[/]|\s', expression) # Ignore this Syntax Warning \s is not a escape here
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
        total.append(sum(new))
        rolls.append(new)
    
    #Now format the String
    end_expr = "Rolls:{},{},{},{},{},{}\nRemoved:{}\nTotal:{}".format(rolls[0], rolls[1], rolls[2], rolls[3], rolls[4], rolls[5], removed_list, total);

    return end_expr

def roll_for_successes(expr):
    #Instead of rolling searching for a sum it receives a expression such as "xdN > Y" (Or opposite xdN < Y)
    #Any other symbol such as +-*/ is invalid

    print(expr)
    invalid = ["+","-","*","/"]
    if any(c in expr for c in invalid): 
        raise Exception("Can only process commands such as 8d10 > 6")

    rolls = getRolls(expr)
    comparison = re.search(r"([<>])\s*(\d+)\s*$", expr)
    sign = comparison.group(1)
    print(sign)
    number = comparison.group(2)
    print(number)

    num_successes = 0
    values = []
    for dice_roll in rolls: 
        rolls, sum_roll = roll_dice(dice_roll)

        if sign == ">": 
            for roll_n in rolls:
                values.append(roll_n)
                num_successes += boolean_c_style(roll_n >= int(number))
        elif sign == "<": 
            for roll_n in rolls:
                values.append(roll_n)
                num_successes += boolean_c_style(roll_n <= int(number))
        else:
            raise "Error"
    return num_successes, int(number), values


def format_roll(expr):
    print(expr)
    # Check for success-based rolls
    if ">" in expr or "<" in expr:
        print("Success Dice? ", expr)

        number_of_successes, objective, values = roll_for_successes(expr)
        message = f"{values} : {number_of_successes} success at difficulty {objective}"
        return number_of_successes, message

    # Check if it's multiple dice rolls without operators
    if is_multiple_dice(expr):
        print("Multiple Dice? ", expr)
        message = roll_multiple_dice(expr)
        return None, message

    # Otherwise, treat as arithmetic expression
    print("Expression Dice? ", expr)

    result, message = roll_expression(expr)
    return result, message


def is_multiple_dice(expr):
    # If there are any arithmetic operators, treat as expression
    if any(op in expr for op in '+-*/'):
        return False
        
    rolls = expr.split()
    return all('d' in part.lower() for part in rolls)



def roll_multiple_dice(expr):
    rolls = expr.split()
    results = []
    for part in rolls:
        roll_results, _ = roll_dice(part)
        print(roll_results)
        results.append(f"{part}({' '.join(map(str, roll_results))}) = {sum(roll_results)}")
    return " |\n ".join(results)


def roll_expression(expr):
    rolls = re.split(r'([+\-*\/])', expr)
    results_string = ""
    message = expr + " = "

    for part in rolls:
        if not part.strip():
            continue
        if part.isdigit():
            results_string += f"{part} "
            message += f"{part} "
        elif 'd' in part.lower():
            roll_results, _ = roll_dice(part)
            results_string += f"({' + '.join(map(str, roll_results))}) "
            message += f"{part}({' '.join(map(str, roll_results))}) [{sum(roll_results)}]"
        else:
            results_string += part + " "
            message += part + " "

    total = calculate(results_string.strip())
    message += f"= :star: {total} :star:"
    return total, message



        
def boolean_c_style(Bool):
    return 1 if Bool else 0

