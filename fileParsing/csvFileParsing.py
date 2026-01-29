import csv

with open("./csvFile.csv", "r") as file:
    data = csv.reader(file, delimiter=" ")
    header = next(data)
    for row in data:
        print(row)

    content = csv.DictReader(file)
    print(list(content))