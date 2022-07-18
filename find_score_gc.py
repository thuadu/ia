import json

keys = []

with open("gc.json") as jsonFile:
    mean = 0
    nbTotal = 0
    data = json.load(jsonFile)
    jsonData = data["entityMentions"]
    for key in jsonData:
        mean+=key["confidence"]
        nbTotal = nbTotal + 1
        #if key.keys()[0] == "confidence": print("IN")
    print(mean/nbTotal)