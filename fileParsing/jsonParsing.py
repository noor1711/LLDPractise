import json
from pprint import pprint

with open("./jsonFile.json", "r") as file:
    content = json.load(file)
    print(content)
    pprint(content)
try:
    with open("./notValid.json", "r") as file:
        content = json.load(file)
        print(content)
except FileNotFoundError:
    print("file not found")
except json.JSONDecodeError:
    print("file not a valid json")

# no need to implicitly close a file when using if 