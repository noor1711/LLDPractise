cc = """
name,branch,year,cgpa
Nikhil,COE,2,9.0
Sanchit,COE,2,9.1
Aditya,IT,2,9.3
Sagar,SE,1,9.5
Prateek,MCE,3,7.8
Sahil,EP,2,9.1
Nikhil,COE,2,9.0
Sanchit,COE,2,9.1
Aditya,IT,2,9.3
Sagar,SE,1,9.5
Prateek,MCE,3,7.8
Sahil,EP,2,9.1
Nikhil,COE,2,9.0
Sanchit,COE,2,9.1
Aditya,IT,2,9.3
Sagar,SE,1,9.5
Prateek,MCE,3,7.8
Sahil,EP,2,9.1
Nikhil,COE,2,9.0
Sanchit,COE,2,9.1
Aditya,IT,2,9.3
Sagar,SE,1,9.5
Prateek,MCE,3,7.8
Sahil,EP,2,9.1
"""

jj = """
{
  "name": "Alice",
  "age": 30,
  "is_student": false,
  "courses": ["Math", "Science"]
}
"""

from pydantic import BaseModel, ValidationError, Field
import csv
import io
import json
from flask import Flask
import typing

app = Flask(__name__)

class Student(BaseModel):
    full_name: str=Field(alias="name")
    branch: str
    cgpa: float=Field(gt=0)

def filter_by_branch(iter_data, field, value):
    filtered_data = []
    for data in iter_data:
        if getattr(data, field) == value:
            filtered_data.append(data)
    return filtered_data

def get_top_students(data, ranking_function):
    return sorted(data, key=ranking_function)

def parse_data(iter_data):
    for data in iter_data:
        try:
            yield Student(**data)
        except ValidationError as e:
            print(f"{e} for {data}")

# lets read the csv file first
with open("csvFile.csv", "r") as csvFile:
    # lets extract all people from COE and then print out the top 10 GPA holder
    data = csv.DictReader(csvFile, delimiter=",")

    def ranking_function(x):
        return -float(getattr(x, "cgpa"))

    top_students:typing.List[Student] = get_top_students(filter_by_branch(parse_data(data), "branch", "COE"), ranking_function)
    json_data = [student.model_dump(by_alias=True) for student in top_students]
    print(json_data)
    
with open("newJsonFile.json", "w") as jsonFile:
    json.dump(json_data, fp=jsonFile, indent=4)


# lets write the same to a csv now
with open("newCsvFile.csv", "w+") as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=["name", "branch", "cgpa"])
    writer.writeheader()
    for row in json_data:
        writer.writerow(row)

with open("stringJsonFile.json", "w") as file:
    json.dump(jj, file, indent=4)


with open("stringCsvFile.csv", "w") as file:
    data = csv.DictReader(io.StringIO(cc), fieldnames="name,branch,year,cgpa".split(","))
    writer = csv.DictWriter(file, fieldnames="name,branch,year,cgpa".split(","))
    writer.writerows(data)