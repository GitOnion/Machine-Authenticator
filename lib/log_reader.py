import json

rawdata = []
with open('Scenario2_log.txt', 'r') as f:
    for line in f.readlines():
        print(line[:-1])
        rawdata.append(json.loads(line[:-1]))
        print(rawdata)
