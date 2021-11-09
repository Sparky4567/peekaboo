from flask import Blueprint
import json
import sqlite3
from config import base_name
from config import admin_base_name
from config import peekaboo_admin
from config import peekaboo_password
from config import db_prefix
from plugins.connector import Base_Connector
import hashlib
create_table_api = Blueprint("create_table_api", __name__)

@create_table_api.route("/ini")
def start_function():
    peekadmin = peekaboo_admin
    peekpassword = peekaboo_password
    peekadmin = hashlib.sha1(str(peekadmin).encode()).hexdigest()
    peekpassword = hashlib.sha1(str(peekpassword).encode()).hexdigest()
    b_a = base_name+db_prefix 
    q_a = """CREATE TABLE IF NOT EXISTS {} (
    id integer PRIMARY KEY AUTOINCREMENT,
    urlaskey text NOT NULL,
    urlvalue text NOT NULL
    );""".format(base_name)
    b_c_a = Base_Connector(b_a,q_a,False,False,False)
    b_c_a.connect_base()
    b_b = admin_base_name+db_prefix
    q_b = """CREATE TABLE IF NOT EXISTS {} (
    id integer PRIMARY KEY AUTOINCREMENT,
    adminname text NOT NULL,
    adminpass text NOT NULL
    );""".format(admin_base_name)
    b_c_b = Base_Connector(b_b,q_b,False,False,False)
    b_c_b.connect_base()
    q_c="""SELECT * FROM {}""".format(admin_base_name)
    b_c_c = Base_Connector(b_b,q_c,False,True,False)
    rows = b_c_c.connect_base()
    
    if len(rows) == 0:
        q_d = """INSERT INTO {} (adminname,adminpass) VALUES ('{}','{}')""".format(admin_base_name,peekadmin,peekpassword)
        b_c = Base_Connector(b_b,q_d,False,False,True)
        b_c.connect_base()
    message = "Data and admin storage created !"
    message = "{}".format(message)
    return json.dumps({"status":message, "length":len(rows)}),200,{'ContentType':'application/json'}
    