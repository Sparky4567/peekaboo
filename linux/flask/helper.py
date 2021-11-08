from flask import Blueprint, json
import sqlite3
import basicauth
from config import admin_base_name
from config import db_prefix
from config import helper_route_enabled
from plugins.connector import Base_Connector

create_helper_api = Blueprint("create_helper_api", __name__)

@create_helper_api.route("/helper")
def listfunction():
    if(helper_route_enabled == True and helper_route_enabled is not None):
        q = """SELECT * FROM {}""".format(admin_base_name)
        b = admin_base_name+db_prefix
        b_c = Base_Connector(b,q,True,False,False)
        row = b_c.connect_base()
        header = basicauth.encode(row[1],row[2])
        message = {"Authorization":header}
    else:
        message = {"Status":"Sorry, this route was disabled"}
    return json.dumps(message),200,{'ContentType':'application/json'}