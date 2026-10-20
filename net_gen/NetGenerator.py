import random

INTERIOR_LOBBY = ["File DV6","Password DV6","Password DV8","Skunk","Wisp","Killer"]
INTERIOR_BASIC = ["Hellhound","Sabertooth","Raven x2" ,"Hellhound","Wisp","Raven","Password DV6" ,"File DV6" ,"Control Node DV6" ,"Password DV6" ,"Skunk","Asp","Scorpion","Killer, Skunk","Wisp x3" ,"Liche"]
INTERIOR_STANDART = ["Hellhound x2","Hellhound, Killer","Skunk x2","Sabertooth","Scorpion","Hellhound","Password DV8","File DV8","Control Node DV8","Password DV8","Asp","Killer","Liche","Asp","Raven x3","Liche, Raven"]
INTERIOR_UNCOMMON = ["Kraken","Hellhound, Scorpion","Hellhound, Killer","Raven x2","Sabertooth","Hellhound","Password DV10","File DV10","Control Node DV10","Password DV10","Killer","Liche","Dragon","Asp, Raven","Dragon, Wisp","Giant"]
INTERIOR_ADVANCED = ["Hellhound x3","Asp x2","Hellhound, Liche","Wisp x3","Hellhound, Sabertooth","Kraken","Password DV12","File DV12","Control Node DV12","Password DV12","Giant","Dragon","Killer, Scorpion","Kraken","Raven, Wisp, Hellhound","Dragon x2"]

DIFFICULTY_INFO = {
    1: "Basic (DV6) | Normal interface level 2",
    2: "Standard (DV8) | Normal interface level 4 | Deadly: 2",
    3: "Uncommon (DV10) | Normal interface level 6 | Deadly: 4",
    4: "Advanced (DV12) | Normal interface level 8 | Deadly: 6"
}

class Floor:
    """A node in a generated NET architecture tree."""

    def __init__(self, level):
        self.level = level
        self.is_edge = True
        self.childs = []
        self.id = 0
        self.occupancy = -1

    def addChild(self, floor):
        self.is_edge = False
        self.childs.append(floor)


class FloorSelector:
    def __init__(self):
        self.selected = [False] * 19

    def getRandom(self):
        rolled = roll3D6()
        while self.selected[rolled]:
            rolled = roll3D6()
        self.selected[rolled] = True
        return rolled

def rollD6():
    return random.randint(1,6)
def rollD10():
    return random.randint(1,10)
def roll3D6():
    return rollD6() + rollD6() + rollD6()


def writePrintOffset(floor,currOffset):
    floor.offset = currOffset
    if floor.is_edge:
        return currOffset
    if len(floor.childs) > 0:
        currOffset = writePrintOffset(floor.childs[0],currOffset)
    for i in range(1,len(floor.childs)):
        currOffset = writePrintOffset(floor.childs[i],currOffset+1)
    return currOffset

# -1 right, -2 down
def printArchitectureMakeConnection(floor, netmap):
    netmap[(floor.level-1)*2][floor.offset*2] = floor.id
    for child in floor.childs:
        for i in range(floor.offset*2+1,child.offset*2):
            netmap[(floor.level-1)*2][i] = -1
        for j in range((floor.level-1)*2+1,(child.level-1)*2):
            netmap[j][child.offset*2] = -2
        printArchitectureMakeConnection(child,netmap)


def printArchitecture(floors):
    output = ""
    depth = 0
    for floor in floors:
        if depth < floor.level:
            depth = floor.level

    print("\nMap:")
    output += "\nMap:\n"
    #findOffsets
    writePrintOffset(floors[0],0)

    #fill grid
    width = 0
    for floor in floors:
        if width <= floor.offset:
            width = floor.offset +1
    netmap = []
    for i in range(0,depth):
        row1 = []
        row2=[]
        for j in range(0,width):
            row1.append(0)
            row2.append(0)
            row1.append(0)
            row2.append(0)
        netmap.append(row1)
        netmap.append(row2)
    # -1 right, -2 down
    printArchitectureMakeConnection(floors[0],netmap)

    for row in netmap:
        strRow = ""
        for hit in row:
            if hit > 0:
                if hit > 9:
                    strRow += str(hit)
                else:
                    strRow += "0"+str(hit)
            if hit == 0:
                strRow += "  "
            if hit == -1:
                strRow += "--"
            if hit == -2:
                strRow += "| " 
        print (strRow)
        output += strRow + "\n"
    return output

'''
# minimal size is 5 for 1 Branche, 
1 entry, 2 second floor, 3 last floor, 4 - nonBranched floor, 5 - 1st possible branch
So maximal branches is: size - 4  
'''
def getNumberOfBraches(size):
    """Roll the number of branches, bounded by the available floor count."""
    max_branches = size - 4
    branch_count = 0
    while branch_count < max_branches:
        if rollD10() >= 5:
            branch_count += 1
        else:
            break
    return branch_count


def findNodeCandidate(all_floors, depth, can_be_edge, can_be_node):
    """Choose an eligible interior node to extend or branch from."""
    candidates = []
    for floor in all_floors:
        if floor.level == 1 or floor.level >= depth - 1:
            continue
        if (floor.is_edge and can_be_edge) or (not floor.is_edge and can_be_node):
            candidates.append(floor)

    # If no eligible interior node exists, continue from the deepest floor.
    if len(candidates) == 0:
        for floor in all_floors:
            if floor.level == depth:
                return floor

    selected_index = random.randint(0, len(candidates) - 1)
    return candidates[selected_index]

def getArchitecture():
    floor_count = roll3D6()
    branch_count = getNumberOfBraches(floor_count)
    print(f"floors:{floor_count} branches:{branch_count}")

    if branch_count > 0:
        minimum_depth = 4
        maximum_depth = floor_count - branch_count
        # Averaging two uniform rolls makes extreme depths less common.
        depth = round((
            random.randint(minimum_depth, maximum_depth)
            + random.randint(minimum_depth, maximum_depth)
        ) / 2)
    else:
        depth = floor_count

    # Build the initial unbranched path from the NET entrance.
    floors = [Floor(1)]
    last_floor = floors[0]
    for level in range(2, depth + 1):
        floor = Floor(level)
        last_floor.addChild(floor)
        floors.append(floor)
        last_floor = floor

    if branch_count > 0:
        remaining_floors = floor_count - depth
        remaining_branches = branch_count
        can_branch_from_node = True
        can_extend_edge = True

        while remaining_floors > 0:
            if remaining_floors == remaining_branches:
                can_extend_edge = False
            if remaining_branches == 0:
                can_branch_from_node = False

            parent_floor = findNodeCandidate(
                floors, depth, can_extend_edge, can_branch_from_node
            )
            if parent_floor.level == depth:
                depth +=1
            if not parent_floor.is_edge:
                remaining_branches -=1
            floor = Floor(parent_floor.level + 1)
            parent_floor.addChild(floor)
            floors.append(floor)
            remaining_floors -=1

    return floors
    
    #for floor in all_floors:
    #	print (f"level:{floor.level},edge:{floor.is_edge},childs:{len(floor.childs)}")
    
def setID(floor,cnt):
    cnt+=1
    floor.id = cnt
    for child in floor.childs:
        cnt = setID(child,cnt)
    return cnt

def setIDs(floors):
    setID(floors[0],0)
    
def populateLevel(floorRandom,floors):
    nextLevel = []
    for floor in floors:
        floor.occupancy = floorRandom.getRandom()
        nextLevel += floor.childs
    if len(nextLevel)>0:
        populateLevel(floorRandom,nextLevel)

def populateFloors(floors):
    first = rollD6()
    second = rollD6()
    while (first==second):
        second = rollD6()
    floor = floors[0]
    floor.occupancy = first
    floor=floor.childs[0]
    floor.occupancy = second

    floorRandom = FloorSelector()
    populateLevel(floorRandom,floor.childs)


def getDificulty():
    print("Please select dificulty")
    print("1-Basic Difficulty    | DV6  | Normal interface level 2 | Deadly bottom inteface level: N/A")
    print("2-Standart Difficulty | DV8  | Normal interface level 4 | Deadly bottom inteface level: 2")
    print("3-Uncommon Difficulty | DV10 | Normal interface level 6 | Deadly bottom inteface level: 4")
    print("4-Advanced Difficulty | DV12 | Normal interface level 8 | Deadly bottom inteface level: 6")
    try:
        dificulty = int(input("Dificulty:"))
    except: 
        print("\n!!ERROR!!")
        print("Provide numbers between 1 and 4")
        print("!!ERROR!!\n")
        return getDificulty()
    if not (dificulty >=1 and dificulty <= 4):
        print("\n!!ERROR!!")
        print("Provide numbers between 1 and 4")
        print("!!ERROR!!\n")
        return getDificulty()
    return dificulty

def printLegend(floors, difficulty):
    output = "**Legend:**\n"  # Add markdown header
    floor = floors[0]	
    output += f"**{floor.id}:** {INTERIOR_LOBBY[floor.occupancy-1]}\n"
    
    floor = floor.childs[0]	
    output += f"**{floor.id}:** {INTERIOR_LOBBY[floor.occupancy-1]}\n"
    
    for child in floor.childs:
        output += printLegendRecursive(child, difficulty)
    return output

def printLegendRecursive(floor, difficulty):
    output = ""
    if difficulty == 1:
        occupancy = INTERIOR_BASIC[floor.occupancy-3]
    elif difficulty == 2:
        occupancy = INTERIOR_STANDART[floor.occupancy-3]
    elif difficulty == 3:
        occupancy = INTERIOR_UNCOMMON[floor.occupancy-3]
    elif difficulty == 4:
        occupancy = INTERIOR_ADVANCED[floor.occupancy-3]
    
    output += f"**{floor.id}:** {occupancy}\n"
    
    for child in floor.childs:
        output += printLegendRecursive(child, difficulty)
    return output


exitApp = False
if __name__ == "__main__":
    while not exitApp:
        difficulty = getDificulty()
        all_floors = getArchitecture()
        setIDs(all_floors)
        populateFloors(all_floors)

        printArchitecture(all_floors)
        printLegend(all_floors,difficulty)


    
