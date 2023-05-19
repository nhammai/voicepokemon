import json

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    # Convert the 'amount' value to an integer
    if "amount" in data:
        data["amount"] = int(data["amount"])

    return data

# Use the function
command = load_json_file('command.json')

print(command)
