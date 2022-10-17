from flask import Flask, url_for, render_template_string, redirect
import sqlite3

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/page/<uuid>")
def render_page(uuid):
    con = sqlite3.connect("db/blog")
    cur = con.cursor()

    res = cur.execute("SELECT uuid_left, uuid_right, content FROM pages WHERE uuid = ?;", (uuid,))

    result = res.fetchone()

    return render_template_string(result[2], left_arrow=url_for("render_page", uuid=result[0]), right_arrow=url_for("render_page", uuid=result[1]))

@app.route("/")
def random_page():
    con = sqlite3.connect("db/blog")
    cur = con.cursor()

    res = cur.execute("SELECT uuid FROM pages ORDER BY RANDOM();")
    result = res.fetchall()

    uuid_list = []
    uuid_list_size = len(result)

    for x in range(uuid_list_size):
        uuid_list.append(result[x][0])
    
    for x in range(uuid_list_size):
        if x == 0:
            data_tuple = (uuid_list[(uuid_list_size - 1)], uuid_list[1], uuid_list[x])
            cur.execute("UPDATE pages SET uuid_left = ?, uuid_right = ? WHERE uuid = ?", data_tuple)
        elif x == (uuid_list_size - 1):
            data_tuple = (uuid_list[(x - 1)], uuid_list[0], uuid_list[x])
            cur.execute("UPDATE pages SET uuid_left = ?, uuid_right = ? WHERE uuid = ?", data_tuple)
        else:
            data_tuple = (uuid_list[(x - 1)], uuid_list[(x + 1)], uuid_list[x])
            cur.execute("UPDATE pages SET uuid_left = ?, uuid_right = ? WHERE uuid = ?", data_tuple)

        first_page = url_for("render_page", uuid=uuid_list[0])

        con.commit()

    return redirect(first_page)




    
    


