import sqlite3
import uuid
from sys import argv

filename = argv[1]
content_tag = argv[2]

f = open(filename, "r")

content = f.read()

data_tuple = (content_tag, content)

con = sqlite3.connect("db/blog-content")
cur = con.cursor()

cur.execute("INSERT INTO pages VALUES (?, ?);", data_tuple)

con.commit()
