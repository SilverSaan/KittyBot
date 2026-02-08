from random import randint
import re
import numpy as np
import random
from Tree import Calc
calculate = Calc.evaluate

DICE_EXPR_FULL = re.compile(
    r'^\s*'
    r'(\d*d\d+(?:\s*[+\-*/]\s*\d+)*'
    r'|\d*d\d+\s*[<>]\s*\d+'
    r'|(?:\d*d\d+\s*)+)'
    r'\s*$',
    re.IGNORECASE
)

def rand(value):
    return randint(1, value)

def roll_dice(dice_string: str) -> tuple:
    """
    Roll dice and return the individual rolls and their sum.
    
    Args:
        dice_string: String in format "NdM" where N is number of dice and M is sides
        
    Returns:
        tuple: (list of individual rolls, sum of rolls)
    """
    dice_part = re.split(r'd|D', dice_string)
    
    if dice_part[0] == '':
        dice_part[0] = '1'

    num_dice = int(dice_part[0])
    num_sides = int(dice_part[1])
    
    if num_sides > 100:
        raise Exception("The Number of sides must not be more than 100")
    if num_dice > 100:
        raise Exception("We don't have that many dice")
    
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    return rolls, sum(rolls)


def getRolls(expression):
    """Extract all dice notation from an expression."""
    x = re.split('[+]|[*]|[-]|[/]|\s', expression)
    rolls = []
    finder = re.compile('[1-9]*[0-9]*(d|D)[1-9][0-9]*')
    for i in range(0, len(x)):
        if finder.match(x[i]): 
            rolls.append(re.search(finder, x[i]).group())
    return rolls


def rollAll(expression):
    """Roll all dice in an expression and return the rolls."""
    rollsexpr = getRolls(expression)
    total = 0
    rolling = []
    for i in range(0, len(rollsexpr)):
        try:
            rolls, result = roll_dice(rollsexpr[i])
        except Exception as e:
            raise Exception(e)
        rolling.append(rolls)
    return rolling, total


def initialScoreRoll(): 
    """
    Roll 6 ability scores using 4d6 drop lowest method.
    
    Returns:
        str: Formatted string with rolls, removed dice, and totals
    """
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
    
    end_expr = "Rolls:{},{},{},{},{},{}\nRemoved:{}\nTotal:{}".format(
        rolls[0], rolls[1], rolls[2], rolls[3], rolls[4], rolls[5], 
        removed_list, total
    )
    return end_expr


def roll_for_successes(expr):
    """
    Roll dice and count successes based on comparison.
    
    Args:
        expr: Expression like "8d10 > 6" or "5d6 < 3"
        
    Returns:
        tuple: (number of successes, target number, list of all roll values, comparison sign)
    """
    invalid = ["+", "-", "*", "/"]
    if any(c in expr for c in invalid): 
        raise Exception("Can only process commands such as 8d10 > 6")

    rolls = getRolls(expr)
    comparison = re.search(r"([<>])\s*(\d+)\s*$", expr)
    sign = comparison.group(1)
    number = int(comparison.group(2))

    num_successes = 0
    values = []
    
    for dice_roll in rolls: 
        roll_results, _ = roll_dice(dice_roll)
        
        for roll_n in roll_results:
            values.append(roll_n)
            if sign == ">": 
                num_successes += boolean_c_style(roll_n >= number)
            elif sign == "<": 
                num_successes += boolean_c_style(roll_n <= number)
    
    return num_successes, number, values, sign


def roll_multiple_dice(expr):
    """
    Roll multiple separate dice expressions.
    
    Args:
        expr: Space-separated dice expressions like "2d6 3d8 1d20"
        
    Returns:
        list: List of tuples (dice_expr, rolls, total) for each dice expression
    """
    rolls = expr.split()
    results = []
    
    for part in rolls:
        roll_results, total = roll_dice(part)
        results.append((part, roll_results, total))
    
    return results


def roll_expression(expr):
    """
    Roll dice in an arithmetic expression and calculate result.
    
    Args:
        expr: Expression like "2d6 + 3" or "1d20 + 5 - 2"
        
    Returns:
        tuple: (total result, list of (dice_expr, rolls, sum) for each dice in expression)
    """
    rolls = re.split(r'([+\-*\/])', expr)
    dice_rolls = []
    calc_string = ""

    for part in rolls:
        if not part.strip():
            continue
        if part.isdigit():
            calc_string += f"{part} "
        elif 'd' in part.lower():
            roll_results, roll_sum = roll_dice(part)
            dice_rolls.append((part, roll_results, roll_sum))
            calc_string += f"({' + '.join(map(str, roll_results))}) "
        else:
            calc_string += part + " "

    total = calculate(calc_string.strip())
    return total, dice_rolls


def is_multiple_dice(expr):
    """Check if expression is multiple dice rolls without operators."""
    if any(op in expr for op in '+-*/'):
        return False
    
    rolls = expr.split()
    return all('d' in part.lower() for part in rolls)


def format_roll(expr):
    """
    Main entry point for rolling dice and formatting the result message.
    
    Args:
        expr: Dice expression to roll
        
    Returns:
        tuple: (numeric result or None, formatted message string)
    """
    # Check for success-based rolls
    if ">" in expr or "<" in expr:
        num_successes, target, values, sign = roll_for_successes(expr)
        operator = ">=" if sign == ">" else "<="
        message = f"{values} : {num_successes} success at difficulty {operator}{target}"
        return num_successes, message

    # Check if it's multiple dice rolls without operators
    if is_multiple_dice(expr):
        results = roll_multiple_dice(expr)
        message_parts = []
        for dice_expr, rolls, total in results:
            rolls_str = ' '.join(map(str, rolls))
            message_parts.append(f"{dice_expr}({rolls_str}) = {total}")
        message = "\n ".join(message_parts)
        return None, message

    # Otherwise, treat as arithmetic expression
    total, dice_rolls = roll_expression(expr)
    print(f"DEBUG: dice_rolls = {dice_rolls}")  # Let's see what's in here

    # Build message
    message = expr + " = " + str(total)
    
    # Substitute dice with rolls
    message = substitute_dice_with_rolls(message, dice_rolls, total)
    message = substitute_rolls_with_sums(message, total)

    return total, message
    
    


def substitute_dice_with_rolls(message, dice_rolls, total):
    """
    Step 1: Replace dice notation with individual rolls.
    "5d10 + 10 = 38" -> "5d10 + 10 = 38\n(3 9 5 1 10) + 10"
    """
    # Convert list of tuples to dict, stripping whitespace from keys
    dice_dict = {dice_expr.strip(): rolls for dice_expr, rolls, _ in dice_rolls}
    
    expr = message.split("=")[0].strip()
    parts = re.split(r'([+\-*\/])', expr)
    
    new_line = ""
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if 'd' in part.lower() and part in dice_dict:
            rolls = dice_dict[part]
            rolls_str = ' '.join(map(str, rolls))
            new_line += f"({rolls_str}) "
        elif part.isdigit():
            new_line += part + " "
        else:
            new_line += part + " "

    new_line = new_line + f" = {total}"
    
    return message + "\n" + new_line.strip()

def substitute_rolls_with_sums(message, total):
    """
    Step 2: Replace roll lists (in parentheses) with their sums.
    "...\n(3 9 5 1 10) + 10" -> "...\n(3 9 5 1 10) + 10\n28 + 10"
    """
    # Get the last line (which has the rolls in parentheses)
    lines = message.split("\n")
    last_line = lines[-1]
    
    # Replace each (x y z) with its sum
    new_line = ""
    i = 0
    while i < len(last_line):
        if last_line[i] == '(':
            # Find closing parenthesis
            j = last_line.index(')', i)
            rolls_str = last_line[i+1:j]
            rolls = [int(x) for x in rolls_str.split()]
            new_line += str(sum(rolls))
            i = j + 1
        else:
            new_line += last_line[i]
            i += 1
    

    return message + "\n" + new_line.strip()


def boolean_c_style(Bool):
    """Convert boolean to 1 or 0."""
    return 1 if Bool else 0