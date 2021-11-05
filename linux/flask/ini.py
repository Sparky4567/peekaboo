from flask import Blueprint
import json
import sqlite3
from config import base_name
from config import admin_base_name
from config import peekaboo_admin
from config import peekaboo_password
from config import db_prefix
create_table_api = Blueprint("create_table_api", __name__)

@create_table_api.route("/ini")
def start_function():
    peekadmin = peekaboo_admin
    peekpassword = peekaboo_password
    conn = sqlite3.connect(base_name+db_prefix) 
    c = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS {} (
    id integer PRIMARY KEY AUTOINCREMENT,
    urlaskey text NOT NULL,
    urlvalue text NOT NULL
    );""".format(base_name)
    c.execute(query)
    conn.close()
    adminconn = sqlite3.connect(admin_base_name+db_prefix)
    d = adminconn.cursor()
    query = """CREATE TABLE IF NOT EXISTS {} (
    id integer PRIMARY KEY AUTOINCREMENT,
    adminname text NOT NULL,
    adminpass text NOT NULL
    );""".format(admin_base_name)
    d.execute(query)
    d.execute("""SELECT * FROM {}""".format(admin_base_name))
    rows = d.fetchall()
    query = """INSERT INTO {} (adminname,adminpass) VALUES ('{}','{}')""".format(admin_base_name,peekadmin,peekpassword)
    if len(rows) == 0:
        d.execute(query)
        d=adminconn.commit()
        adminconn.close()
    message = "Data and admin storage created !"
    message = "{}".format(message)
    return json.dumps({"status":message, "length":len(rows)}),200,{'ContentType':'application/json'}
    