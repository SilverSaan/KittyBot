import json

#This was made to parse stat tables into JSON Objects
def parse_table(table):
    # Split the table by lines
    lines = table.strip().split('\n')
    
    # Initialize an empty list to store dictionaries for each line
    result = []

    # Iterate over each line
    for line in lines:
        # Split the line by spaces
        parts = line.strip().split()

        # Create a dictionary for the line
        entry = {
            "int": int(parts[1]),
            "ref": int(parts[2]),
            "dex": int(parts[3]),
            "tech": int(parts[4]),
            "cool": int(parts[5]),
            "will": int(parts[6]),
            "luck": int(parts[7]),
            "move": int(parts[8]),
            "body": int(parts[9]),
            "emp": int(parts[10])
        }

        # Append the dictionary to the result list
        result.append(entry)

    # Return the list of dictionaries as a JSON object
    return '[\n' + ',\n'.join(json.dumps(entry, indent=None) for entry in result) + '\n]'

# Example table
# Pure copy paste from the book
table = """
1 6 6 8 3 6 7 6 6 6 4
2 5 7 6 5 8 8 8 7 5 4
3 5 8 6 3 8 7 6 5 6 5
4 5 8 7 4 8 6 7 7 7 5
5 6 6 6 3 6 7 6 7 7 4
6 7 6 8 4 6 7 6 5 6 5
7 6 7 8 4 6 6 7 5 7 5
8 5 7 8 3 8 6 7 5 5 5
9 6 7 6 4 8 6 6 6 6 6
10 5 6 7 4 7 8 7 7 7 4
"""

# Parse the table and print the JSON object
print(parse_table(table))