import json

keys = []

with open("azure.json") as jsonFile:
    mean = 0
    nbTotal = 0
    data = json.load(jsonFile)
    jsonData = data["documents"]
    for key in jsonData[0]["entities"]:
        mean+=key["confidenceScore"]
        nbTotal = nbTotal + 1
        #if key.keys()[0] == "confidence": print("IN")
    print(mean/nbTotal)