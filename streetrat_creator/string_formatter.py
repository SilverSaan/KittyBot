
def uppercase_first_letter(string: str): 
    return string[0].upper() + string[1:]

def format_skills(i_class:dict): 
    
    result = ""
    for key, value in i_class.items():
        result += f"{uppercase_first_letter(key)} : {value}, "
        
    return result

def format_stats(stats): 
    
    stats_t = f"""
```
╔══════╤═════╤═════╤══════╤══════╗
║ BODY │ REF │ DEX │ MOVE │ WILL ║
╠══════╪═════╪═════╪══════╪══════╣
║ {stats['body']}    │ {stats['ref']}   │ {stats['dex']}   │ {stats['move']}    │ {stats['will']}    ║
╚══════╧═════╧═════╧══════╧══════╝

╔══════╤══════╤══════╤═════╤═════╗
║ TECH │ COOL │ LUCK │ INT │ EMP ║
╠══════╪══════╪══════╪═════╪═════╣
║ {stats['tech']}    │ {stats['cool']}    │ {stats['luck']}    │ {stats['int']}   │ {stats['emp']}   ║
╚══════╧══════╧══════╧═════╧═════╝
```
"""

    return stats_t   


    
def string_result(role, hp, humanity, role_skill, stats, skills):
    result = f"Selected role: {role}\nHP: {hp}\nHumanity: {humanity}\nStats: {format_stats(stats)}Role Skill: {role_skill}\n" + f"Skills: \n{format_skills(skills[role.lower()])}"
    return result