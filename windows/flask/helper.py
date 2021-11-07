from flask import Blueprint, json
import sqlite3
import basicauth
from config import admin_base_name
from config import db_prefix
from plugins.connector import Base_Connector

create_helper_api = Blueprint("create_helper_api", __name__)

@create_helper_api.route("/helper")
def listfunction():
    q = """SELECT * FROM {}""".format(admin_base_name)
    b = admin_base_name+db_prefix
    b_c = Base_Connector(b,q,True,False,False)
    row = b_c.connect_base()
    header = basicauth.encode(row[1],row[2])
    return json.dumps([{"Authorization":header}]),200,{'ContentType':'application/json'}