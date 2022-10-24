import sqlite3
import json

con = sqlite3.connect("db/blog")
cur = con.cursor()

res = cur.execute("SELECT tag, adjacents FROM network;")

result = res.fetchall()

network = []

for x in result:
    node = {"tag":x[0], "adjacents":x[1].split("|")}
    network.append(node)

pairs = []

for node in network:
    for adj in node["adjacents"]:
        pair = [node["tag"], adj]
        pair.sort()
        if (pair not in pairs):
            pairs.append(pair)


print(json.dumps(pairs))
        
print(json.dumps(network))

