from flask import Flask, url_for, render_template_string, redirect, jsonify, request, send_from_directory
import sqlite3
import os

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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

@app.route("/dbnet")
def dbnet_json():
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
    
    net_data = {"nodes":network, "edges":pairs}

    return jsonify(net_data)

@app.route("/netsave", methods = ['POST'])
def netsave_json():
    return request.get_json(force=True)



    
    


