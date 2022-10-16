import sqlite3
import uuid
from sys import argv
import argparse

parser=argparse.ArgumentParser(description="Inserts html file content into sqlite database with the given name")

parser.add_argument('filename', help='Filename of html/text file')
parser.add_argument('tag', help='Tag for html/text in the database')

args = parser.parse_args()

f = open(args.filename, "r")

content = f.read()

data_tuple = (args.tag, content)

con = sqlite3.connect("db/blog-content")
cur = con.cursor()

cur.execute("INSERT INTO pages VALUES (?, ?);", data_tuple)

con.commit()
