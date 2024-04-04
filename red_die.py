#This archive dice rolls with the Cyberpunk Red Rules
import re
import Dice_Processing as dp 
import json

def format_roll(expr):
    rolls = re.split(r'([+\-*\/])', expr)
    results_string = ""
    message_to_user = expr + " = "
    critical = False
    add_d10 = False
    sub_d10 = False
    
    
    for part in rolls:
        if part.strip():
            if part.isdigit():  # If it's a constant number
                results_string += f"{part} "
                message_to_user += f"{part} "
            elif 'd' in part or 'D' in part:  # If it's a dice roll
                if 'd6' in part or 'D6' in part or 'd10' in part or 'D10' in part: 
                    roll_results, _ = dp.roll_dice(part)
                    if 'd10' in part or 'D10' in part:  # Check if it's a d10 roll
                        if 10 in roll_results:  # Check if result contains 10
                            add_d10 = True  # Add another d10 roll
                        elif 1 in roll_results:  # Check if result contains 1
                            sub_d10 = True # Subtract another d10 roll
                    if 'd6' in part or 'D6' in part:  # Check if it's a d6 roll
                        if roll_results.count(6) >= 2:  # Check if there are 2 or more 6's
                            critical = True  # Set critical variable to true
                    results_string += f"({' + '.join(map(str, roll_results))}) "
                    message_to_user += f"{part}({' '.join(map(str, roll_results))}) "
                    if add_d10: 
                        value = dp.roll_dice("1d10")[0][0]
                        results_string += f'+ {value}'
                        message_to_user += f'CRIT :bangbang: {{+1d10({value})}} '
                        
                    elif sub_d10:
                        value = dp.roll_dice("1d10")[0][0]
                        if value == 10:
                            special_sentence_request = "Preem! A 10!! ...oh shit! :skull:"
                        else:
                            special_sentence_request = ""
                        results_string += f'- {value}'
                        message_to_user += f'You got unlucky choom :pensive: {{-1d10({value}{special_sentence_request})}} '
                        
                else:
                    return None, "Invalid roll. Only rolls for multiple d6's and d10's are allowed, choom", None, 
            else:  # If it's an operator
                results_string += part + " "
                message_to_user += part + " "
    result = dp.calculate(results_string.strip())
    if add_d10:
        message_to_user += f"= :boom: {result} :boom:"
    elif sub_d10:
        message_to_user += f"= :melting_face: {result} :melting_face:"
    else:
        message_to_user += f"= :star: {result} :star:"
    return results_string.strip(), message_to_user.strip(), critical


def test_format_roll():
    # Test case: Roll 4d6
    result_str, message, critical, result = format_roll("4d6")
    assert result >= 4 and result <= 24, "Incorrect result for 4d6 roll"
    assert "4d6" in message, "Message does not contain original roll expression"
    assert ":star:" in message, "Message does not contain result symbol"
    print("Message to user:", message)
    print("Critical:", critical)
    print("Result:", result)
    
    # Test case: Roll 1d10
    result_str, message, critical, result = format_roll("1d10")
    print("Message to user:", message)
    print("Critical:", critical)
    print("Result:", result)
    assert "1d10" in message, "Message does not contain original roll expression"
    assert ":star:" in message, "Message does not contain result symbol"
    assert not critical, "Critical variable should be False for 1d10 roll"
    print("All test cases passed successfully.")


def get_injuries():
    body_crits = None
    head_crits = None
    with open('critical_injury/body_crits.json') as f:
        body_crits = json.load(f)
    with open('critical_injury/head_crits.json') as f:
        head_crits = json.load(f)
        
    return body_crits, head_crits

body_crits, head_crits = get_injuries()


def get_random_injury(injury_effects):
    import random
    roll_result = random.randint(1, 6) + random.randint(1, 6) - 2 # -2 to map with the 11 possible results [0] to [10]
    roll_result = min(roll_result, len(injury_effects) - 1)    
    return list(injury_effects.keys())[roll_result]
    

def get_body_injury():
    
    critical_message = "Body Critical Injury!\n"
    injury = get_random_injury(body_crits)
    critical_message += injury + "\n"
    critical_message += "Quick Fix: " + body_crits[injury]["Quick Fix"] + "\n"
    critical_message += "Treatment: " + body_crits[injury]["Treatment"] + "\n\n"

    critical_message += "Effect: " + body_crits[injury]["Effect"]
    
    return critical_message


def get_head_injury(): 
    critical_message = "Head Critical Injury!\n"
    injury = get_random_injury(head_crits)
    critical_message += injury + "\n"
    critical_message += "Quick Fix: " + head_crits[injury]["Quick Fix"] + "\n"
    critical_message += "Treatment: " + head_crits[injury]["Treatment"] + "\n\n"

    critical_message += "Effect: " + head_crits[injury]["Effect"]
    
    return critical_message


def red(expr):
    critical_message = None
    _, message, crit = format_roll(expr)
    if(crit):
        critical_message = "Critical Damage!! :skull:\n"
        critical_message += "I'm assuming you were aiming for your enemy's body, if you want me to roll a head critical injury use /crithead\n\n"
        injury = get_random_injury(body_crits)
        critical_message += injury + "\n"
        critical_message += "Quick Fix: " + body_crits[injury]["Quick Fix"] + "\n"
        critical_message += "Treatment: " + body_crits[injury]["Treatment"] + "\n\n"
        critical_message += "Effect: " + body_crits[injury]["Effect"]
        
    return message, critical_message
    

