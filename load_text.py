import sqlite3
import uuid
from sys import argv

filename = argv[1] 

f = open(filename, "r")

content = f.read()

uid = str(uuid.uuid4())

data_tuple = (uid, content)

con = sqlite3.connect("db/blog-content")
cur = con.cursor()

cur.execute("INSERT INTO pages VALUES (?, ?);", data_tuple)

con.commit()
