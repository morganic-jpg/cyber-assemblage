import sqlite3
from sys import argv

filename = argv[0] 

f = open(filename, "r")

print(f.read())

con = sqlite3.connect("db/blog-content")
cur = con.cursor()

cur.execute(f"INSERT INTO pages content VALUES {f.read()}")

con.commit()
