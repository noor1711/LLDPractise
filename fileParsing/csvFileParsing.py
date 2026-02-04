import csv

with open("./csvFile1.csv", "w+") as file:
    # data = csv.reader(file, delimiter=" ")
    # header = next(data)
    # for row in data:
    #     print(row)

    with open("./csvFile.csv", "+r") as readFile:
        content = csv.DictReader(readFile)
        content = list(content)
        print(content)
    writer = csv.DictWriter(file, fieldnames=list(content[0].keys()))
    writer.writeheader()
    writer.writerows([*content, *content])