import sqlite3
import argparse
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

parser=argparse.ArgumentParser(description="Inserts html file content into sqlite database with the given name")

parser.add_argument('filename', help='Filename of html/text file')
parser.add_argument('tag', help='Tag for html/text in the database')

args = parser.parse_args()

f = open(args.filename, "r")

content = f.read()

uuid = id_generator(10)

data_tuple = (uuid, args.tag, content)

con = sqlite3.connect("db/blog")
cur = con.cursor()

cur.execute("INSERT INTO pages (uuid, tag, content) VALUES (?, ?, ?);", data_tuple)

con.commit()
