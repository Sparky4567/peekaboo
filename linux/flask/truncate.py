import flask
from flask.app import Flask
from config import admin_base_name
from config import base_name
from config import db_prefix
import json
import sqlite3
import basicauth
from plugins.connector import Base_Connector
create_truncate_api = flask.Blueprint('create_truncate_api',__name__)

@create_truncate_api.route("/truncate")
def truncate_function():
    headers = flask.request.headers
    auth_string =  headers.get("Authorization")
    if(auth_string is not None):
        b = admin_base_name+db_prefix
        q = "SELECT * FROM {}".format(admin_base_name)
        b_c = Base_Connector(b,q,True,False,False)
        row = b_c.connect_base()
        base_auth= basicauth.encode(row[1],row[2])
        if(auth_string==base_auth):
            b = base_name+db_prefix
            q = "DELETE FROM {}".format(base_name)
            b_c = Base_Connector(b,q,False,False,True)
            b_c.connect_base()
            status = True
            return json.dumps({"status":status}),200,{'ContentType':'application/json'}
            
        else:
            return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}
        
    else:
        return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}