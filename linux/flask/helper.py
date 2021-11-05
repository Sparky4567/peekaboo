from flask import Blueprint, json
import sqlite3
import basicauth
from config import admin_base_name
from config import db_prefix

create_helper_api = Blueprint("create_helper_api", __name__)

@create_helper_api.route("/helper")
def listfunction():
    listconn = sqlite3.connect(admin_base_name+db_prefix)
    sel = listconn.cursor()
    sel.execute("""SELECT * FROM {}""".format(admin_base_name))
    row = sel.fetchone()
    header = basicauth.encode(row[1],row[2])
    return json.dumps([{"Authorization":header}]),200,{'ContentType':'application/json'}