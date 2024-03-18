style = [
    "Clean, Professional, Attractive, and Fashionable",
    "Dark, Cloaked, Secretive, and Shadowed",
    "Huge, Intimidating, with a Scary Look in Their Eye",
    "Small and Unassuming, but With a Hint of Danger",
    "Flashy, Bright, and Loud with a lot of Fashionware",
    "Chromed Up and Inhuman",
    "Creepy, Off-Putting, and Alarming",
    "Tastefully Stylish, with Subtle Hints at Wealth",
    "Casual and Relaxed, without much Style",
    "Crazy and Wild, With No Discernable Style"
]

personality = [
    "Professional and Business-Like",
    "Curt, Stoic, and Serious At All Times",
    "Aggressive, Angry, and Ready for Violence",
    "Quiet, Observant, and Contemplative",
    "Crazy and All Over the Place",
    "Cool, Smooth, and Soft-Spoken",
    "Fast-Paced, Impatient, and Arrogant",
    "Loud, Boisterous, and the Center of Attention",
    "Relaxed, Joking, and Fun-Loving",
    "Secretive, Doubting, and a Little Paranoid"
]

secret = [
    "They're secretly in debt to or working for someone else.",
    "They're more/less important than they claim or seem to be.",
    "Someone very powerful wants them dead.",
    "They know secrets about one or more of the PC's.",
    "They are related to/involved in one of the PC's love story.",
    "They are friends with one of the PC's enemies.",
    "They are enemies of one of the PC's friends.",
    "They own or have something very important or valuable.",
    "They're dealing with someone they'd rather not admit to.",
     "They're actually someone else, hiding their true identity."
]

goal = [
    "They want the PC's help to settle a score or debt.",
    "They need something that the PC's have.",
    "They want to give or sell something to the PC's.",
    "They are trying to kill or ruin one or more of the PC's.",
    "They are trying to get to someone else that the PC's know.",
    "They want to complete a job given to them by someone else.",
    "They want someone captured or killed.",
    "They want to go somewhere they currently cannot go.",
    "They are trying to uncover a big secret.",
    "They are trying to recover something they lost."
]

skills = [
    "A tough hired gun that can kill at a moment's notice.",
    "A deadly assassin that can tag a target anywhere, anytime.",
    "A burglar/infiltrator that can get into and out of anywhere.",
    "A netrunner/hacker that can break any system.",
    "A technician that knows your hardware better than you do.",
    "An underground medic with the skills to keep you alive.",
    "A driver who can make the cops heads spin with style.",
    "An augmented super-soldier with deadly cyber-weapons.",
    "A martial arts master than can kill with their bare hands.",
    "An explosive saboteur with a reputation for destruction."
]

meeting_spot = [
    "A popular club, nightclub, or bar.",
    "A brightly lit street corner, with people around.",
    "A dark or secluded alleyway, where no one will hear you.",
    "A small diner or bar tucked in an out-of-the-way place.",
    "A shack or container on the outskirts of town.",
    "A refurbished room of an abandoned building.",
    "Their residence that actually looks clean.",
    "A repurposed warehouse or factory.",
    "An underground tunnel or basement of another building.",
    "A room high up in a tower, skyscraper, or megabuilding."
]


def get_merc():
    return {
        'style': style,
        'personality': personality,
        'goal': goal,
        'secret': secret,
        'skills': skills,
        'meeting_spot': meeting_spot
    }
    
#Run a test if called as main
if __name__ == "__main__":
    import random
    npc_data = get_merc()
    print("Your Mercenary is:")
    res_style = random.choice(npc_data['style'])
    res_personality = random.choice(npc_data['personality'])
    res_secret = random.choice(npc_data['secret'])
    res_goal = random.choice(npc_data['goal'])
    res_skills = random.choice(npc_data['skills'])
    res_spot = random.choice(npc_data['meeting_spot'])
    print(res_personality)
    print("They appear", res_style)
    print("They are a", res_skills)
    print("You met at", res_spot)
    print("They hide that", res_secret)
    print(res_goal)
    