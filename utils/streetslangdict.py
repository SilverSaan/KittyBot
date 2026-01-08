import random

# Cyberpunk streetslang dictionary
STREETSLANG = {
    "choom": "Friend, buddy, pal",
    "choomba": "Close friend, trusted companion",
    "gonk": "Idiot, fool, someone who screwed up",
    "preem": "Premium, excellent, top quality",
    "nova": "Cool, awesome, amazing",
    "klep": "To steal",
    "eddies": "Eurodollars, money",
    "eurodollars": "Standard currency, eddies",
    "flatline": "To die, to kill someone",
    "chrome": "Cyberware, cybernetic enhancements",
    "borg": "Full conversion cyborg, someone with extensive chrome",
    "ripper": "Ripperdoc, underground cyberware surgeon",
    "ripperdoc": "Underground surgeon who installs cyberware",
    "netrunner": "Hacker who jacks into the Net",
    "runner": "Short for netrunner",
    "solo": "Mercenary, hired gun, combat specialist",
    "fixer": "Middleman, dealer, someone who arranges jobs",
    "corpo": "Corporate employee, usually derogatory",
    "rat": "Corporate spy or informant",
    "ice": "Intrusion Countermeasures Electronics, security software",
    "deck": "Cyberdeck, hacking equipment",
    "jack in": "To connect to the Net via neural interface",
    "braindance": "Recorded experience played back directly to the brain",
    "bd": "Short for braindance",
    "slot": "Verb: to kill; Exclamation: damn",
    "scop": "To scope out, to surveil, to check something out",
    "zero": "To kill someone",
    "chippin' in": "Using a skill chip or getting involved",
    "input": "Opinion, advice, what someone thinks",
    "output": "Response, reaction, what someone says",
    "static": "Trouble, interference, problems",
    "buzz": "News, information, rumor",
    "max": "Maximum, the best, topped out",
    "delta": "To leave quickly, to run away",
    "icy": "Cold-hearted, ruthless, dangerous",
    "juice": "Electricity, power, or influence",
    "handle": "Nickname, street name",
    "meat": "Physical body (as opposed to virtual)",
    "iron": "Gun, firearm",
    "boost": "To steal, or to enhance with drugs/chrome",
    "burn": "To betray, to expose someone",
    "chiphead": "Someone addicted to braindances or chips",
    "cred": "Street credibility, reputation",
    "street cred": "Your reputation on the streets",
    "edge": "Advantage, or living on the margin",
    "face": "Reputation, or a recognizable person",
    "ganic": "Organic, not cybered up",
    "hopper": "Flying vehicle, usually an AV",
    "av": "Aerodyne vehicle, flying car",
    "jamming": "Moving fast, or interfering",
    "kibble": "Cheap processed food",
    "motor": "To move, to leave",
    "output": "Leave, get out",
    "rock": "To do well, to excel",
    "scratch": "Money, eddies",
    "shiny": "New, attractive, good looking",
    "slotted": "Killed, dead",
    "chrome dome": "Someone with obvious head cyberware",
    "samurai": "Elite solo, warrior",
    "joytoy": "Prostitute",
    "doll": "Joytoy, usually one in a dollhouse",
    "booster": "Gang member, usually a cyberpsycho gang",
    "boostergang": "Violent gang of cybered-up thugs",
    "tech": "Technician, or technology",
    "Mr. Studd": "Popular sexual-enhancement cyberware",
    "midnight lady": "Female version of Mr. Studd",
    "sandy": "Sandevistan, reflex-boosting cyberware",
    "kerenzikov": "Reflex booster cyberware",
    "smasher": "Adam Smasher, or anyone heavily borged out",
    "tinman": "Derogatory term for heavily cybered person",
    "meat puppet": "Someone being controlled, or a joytoy",
    "screamer": "Alarm, or someone who panics",
    "screamsheet": "Sensationalist newspaper",
    "vidiot": "Someone addicted to video/braindance",
    "wizard": "Expert netrunner",
    "zetatech": "Major corporation known for biotech",
    "arasaka": "Mega-corporation, Japanese security and manufacturing",
    "militech": "Mega-corporation, American military contractor",
    "biotechnica": "Mega-corporation, bioengineering and agriculture",
    "night city": "The main city, free city on California coast",
    "pacifica": "Dangerous district of Night City, combat zone",
    "combat zone": "Lawless area controlled by gangs",
    "hot zone": "Dangerous area, combat zone",
    "the street": "The urban environment, street culture",
    "edge of night": "The dangerous side of the city",
    "little china": "Asian district in Night City",
    "japantown": "Japanese district in Night City",
    "corp plaza": "Corporate center district",
    "badlands": "Wasteland outside the city",
    "nomad": "Wanderer, lives outside cities",
    "pack": "Nomad clan or family",
    "rockerboy": "Rebel musician with a message",
    "media": "Reporter, journalist with ethics",
    "lawman": "Cop, law enforcement",
    "exec": "Corporate executive",
    "med tech": "Medical technician",
    "techie": "Technical expert, mechanic",
    "gleam": "To understand, to get it",
    "gray": "Uncertain, morally ambiguous",
    "red": "Dangerous, violent, bloody",
    "black": "Illegal, illicit, underground",
    "white": "Legal, legitimate, corporate",
    "blaze": "To shoot, to fire a weapon",
    "chill": "To relax, or to kill",
    "chippin'": "Using chips or getting high",
    "cooler": "Prison, jail",
    "cryo": "Cryogenic storage, or very cool",
    "dig": "To understand, to like",
    "eddies": "Money, eurodollars",
    "wire": "Nerves, nervous system, or information",
    "wired": "Nervous, tense, or connected",
    "juice head": "Steroid user or cyberware addict",
    "toy": "Gun, weapon",
    "bang": "To shoot",
    "clip": "Magazine of ammunition",
    "heater": "Gun, weapon",
    "piece": "Gun",
    "scatter": "Shotgun",
    "chooh2": "Synthetic fuel for vehicles",
    "synthcoke": "Synthetic cocaine",
    "black lace": "Deadly drug, causes time distortion",
    "blue glass": "Hallucinogenic drug",
    "smash": "Amphetamine-based drug",
    "boost": "Performance-enhancing drug",
    "speedheal": "Rapid healing drug",
    "dorph": "Pain killer, endorphin blocker",
    "program": "Netrunning software",
    "daemon": "Autonomous ICE program",
    "soulkiller": "Deadly ICE program that destroys minds",
    "quickhack": "Fast netrunning attack program",
    "heathen": "Non-religious person, normal person",
    "Adam Smasher": "Legendary full-borg solo, now more machine than man",
    "Johnny Silverhand": "Legendary rockerboy, anti-corporate rebel"
}

def lookup_slang(term):
    """
    Look up a streetslang term and return its definition.
    Returns None if term not found.
    """
    term_lower = term.lower().strip()
    if term_lower in STREETSLANG:
        term_to_send = term_lower.capitalize()
        return f"**{term_to_send}**: {STREETSLANG[term_lower]}"
    return None

def random_slang():
    """
    Return a random streetslang term and its definition.
    """
    term = random.choice(list(STREETSLANG.keys()))
    return f"**{term}**: {STREETSLANG[term]}"

def search_slang(query):
    """
    Search for terms containing the query string.
    Returns list of matching terms with definitions.
    """
    query_lower = query.lower().strip()
    matches = []
    
    for term, definition in STREETSLANG.items():
        if query_lower in term or query_lower in definition.lower():
            matches.append(f"**{term}**: {definition}")
    
    return matches

def list_all_slang():
    """
    Return all streetslang terms in alphabetical order.
    """
    sorted_terms = sorted(STREETSLANG.items())
    return [f"**{term}**: {definition}" for term, definition in sorted_terms]

def get_slang_count():
    """
    Return the total number of slang terms in the dictionary.
    """
    return len(STREETSLANG)