import json

with open("roj_dan_tekmovalcev.json", "r+") as jsonDat:
    podatki = json.load(jsonDat)

    for podatek in podatki:
        datum = podatek["datum"]
        dan = datum[:2]
        mesec = datum[3:5]
        leto = datum[-4:]
        podatek["datum"] = leto + "-" + mesec + "-" + dan

    jsonDat.seek(0)
    json.dump(podatki, jsonDat)
    jsonDat.truncate()
