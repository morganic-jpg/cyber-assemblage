import sqlite3

con = sqlite3.connect("db/blog-content")
cur = con.cursor()

res = cur.execute("SELECT count(*) FROM pages;")

page_count = (res.fetchone())[0]

res = cur.execute("SELECT content FROM pages ORDER BY RANDOM();")
content_list = res.fetchall()

for x in range(page_count):
    page_num = x + 1
    f = open(f"{page_num}.html", "w")
    content_string = content_list[x][0]

    if (page_num == 1):
        content_string = content_string.replace("rightarrowbuttonlink", f"{page_num + 1}.html")
        content_string = content_string.replace("leftarrowbuttonlink", f"{page_count}.html")
    elif (page_num == page_count):
        content_string = content_string.replace("rightarrowbuttonlink", f"1.html")
        content_string = content_string.replace("leftarrowbuttonlink", f"{page_num - 1}.html")
    else:
        content_string = content_string.replace("rightarrowbuttonlink", f"{page_num + 1}.html")
        content_string = content_string.replace("leftarrowbuttonlink", f"{page_num - 1}.html")

    f.write(content_string)
