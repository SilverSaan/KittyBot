
def uppercase_first_letter(string: str): 
    return string[0].upper() + string[1:]

def format_skills(i_class:dict): 
    
    result = ""
    for key, value in i_class.items():
        result += f"{uppercase_first_letter(key)} : {value}, "
        
    return result

def format_stats(stats): 
    stats_s = "\n"
    stats_s += f"INT: {stats['int']}\n"    
    stats_s += f"REF: {stats['ref']}\n"    
    stats_s += f"DEX: {stats['dex']}\n"    
    stats_s += f"TECH: {stats['tech']}\n"    
    stats_s += f"COOL: {stats['cool']}\n"    
    stats_s += f"WILL: {stats['will']}\n"    
    stats_s += f"LUCK: {stats['luck']}\n"    
    stats_s += f"MOVE: {stats['move']}\n"    
    stats_s += f"BODY: {stats['body']}\n"    
    stats_s += f"EMP: {stats['emp']}\n" 
    
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