def read_command(filename):
    # Open the file for reading
    with open(filename, "r") as f:
        # Read the contents of the file
        contents = f.read()

    # Split the contents of the file by line
    lines = contents.split("\n")

    # Create an empty dictionary to store the command and amount
    command = {}

    # Loop through each line in the file
    for line in lines:
        # Split the line by the colon character
        parts = line.split(":")
        
        # Check if the line contains the command or amount
        if parts[0].strip() == "Command":
            # If it's the command, store it in the dictionary under the "skill" key
            command["skill"] = parts[1].strip()
        elif parts[0].strip() == "Amount":
            # If it's the amount, convert it to an integer and store it in the dictionary under the "amount" key
            command["amount"] = int(parts[1].strip())

    # Return the resulting dictionary
    return command


from understand_command import read_command
