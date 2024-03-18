#This archive dice rolls with the Cyberpunk Red Rules
import re
import Dice_Processing as dp 

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
                        message_to_user += f'CRIT :bangbang: {{+1d10({value})}}'
                    elif sub_d10:
                        value = dp.roll_dice("1d10")[0][0]

                        results_string += f'- {value}'
                        message_to_user += f'You got unlucky choom :pensive: {{-1d10({value})}}'
                else:
                    return None, "Invalid roll. Only rolls for multiple d6's and d10's are allowed, choom", None, 
            else:  # If it's an operator
                results_string += part + " "
                message_to_user += part + " "
    result = dp.calculate(results_string.strip())
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


injury_effects = {
    "Dismembered Arm": {
        "Effect": "The Dismembered Arm is gone. You drop any items in that dismembered arm's hand immediately. Base Death Save Penalty is increased by 1.",
        "Quick Fix": "N/A",
        "Treatment": "Surgery DV17"
    },
    "Dismembered Hand": {
        "Effect": "The Dismembered Hand is gone. You drop any items in the dismembered hand immediately. Base Death Save Penalty is increased by 1.",
        "Quick Fix": "N/A",
        "Treatment": "Surgery DV17"
    },
    "Collapsed Lung": {
        "Effect": "-2 to MOVE (minimum 1). Base Death Save Penalty is increased by 1.",
        "Quick Fix": "Paramedic DV15",
        "Treatment": "Surgery DV15"
    },
    "Broken Ribs": {
        "Effect": "At the end of every Turn where you move further than 4m/yds on foot, you re-suffer this Critical Injury's Bonus Damage directly to your Hit Points.",
        "Quick Fix": "Paramedic DV13",
        "Treatment": "Paramedic DV15 or Surgery DV13"
    },
    "Broken Arm": {
        "Effect": "The Broken Arm cannot be used. You drop any items in that arm's hand immediately.",
        "Quick Fix": "Paramedic DV13",
        "Treatment": "Paramedic DV15 or Surgery DV13"
    },
    "Foreign Object": {
        "Effect": "At the end of every Turn where you move further than 4m/yds on foot, you re-suffer this Critical Injury's Bonus Damage directly to your Hit Points. Quick Fix removes Injury Effect permanently.",
        "Quick Fix": "First Aid or Paramedic DV13",
        "Treatment": "Quick Fix removes Injury Effect permanently"
    },
    "Broken Leg": {
        "Effect": "-4 to MOVE (minimum 1).",
        "Quick Fix": "Paramedic DV13",
        "Treatment": "Paramedic DV13, Paramedic DV15 or Surgery DV13"
    },
    "Torn Muscle": {
        "Effect": "-2 to Melee Attacks. Quick Fix removes Injury Effect permanently.",
        "Quick Fix": "First Aid or Paramedic DV13",
        "Treatment": "Quick Fix removes Injury Effect permanently"
    },
    "Spinal Injury": {
        "Effect": "Next Turn, you cannot take an Action, but you can still take a Move Action. Base Death Save Penalty is increased by 1.",
        "Quick Fix": "Paramedic DV15",
        "Treatment": "Surgery DV15"
    },
    "Crushed Fingers": {
        "Effect": "-4 to all Actions involving that hand.",
        "Quick Fix": "Paramedic DV11",
        "Treatment": "Surgery DV15"
    },
    "Dismembered Leg": {
        "Effect": "The Dismembered Leg is gone. -6 to MOVE (minimum 1). You cannot dodge attacks. Base Death Save Penalty is increased by 1.",
        "Quick Fix": "N/A",
        "Treatment": "Surgery DV15"
    }
}


def get_random_injury(injury_effects):
    import random
    return random.choice(list(injury_effects.keys()))


def red(expr):
    critical_message = None
    _, message, crit = format_roll(expr)
    if(crit):
        critical_message = "Critical Damage!! :skull:\n"
        critical_message += "I'm assuming you were aiming for your enemy's body, if you want me to roll a head critical injury use /crithead\n\n"
        injury = get_random_injury(injury_effects)
        critical_message += injury + "\n"
        critical_message += "Effect:" + injury_effects[injury]["Effect"]
        
    return message, critical_message
    

