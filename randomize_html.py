import sqlite3

con = sqlite3.connect("db/blog-content")
cur = con.cursor()

res = cur.execute("SELECT count(*) FROM pages;")

page_count = res.fetchone()

res = cur.execute("SELECT tag FROM pages ORDER BY RAND();")
tag_list = res.fetchall()

print(page_count)
print(tag_list)

#count_list = range(page_count)

#for x in count_list:

