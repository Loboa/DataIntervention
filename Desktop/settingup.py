import json

file=open("database.txt")
s=json.load(file)
names=s["Grade 12 _____A-E"]["database"]
print(names)
