import flask
from config import admin_base_name
from config import base_name
import json
import sqlite3
import basicauth
create_truncate_api = flask.Blueprint('create_truncate_api',__name__)

@create_truncate_api.route("/truncate")
def truncate_function():
    headers = flask.request.headers
    auth_string =  headers.get("Authorization")
    if(auth_string is not None):
        auth_conn = sqlite3.connect(admin_base_name)
        sel = auth_conn.cursor()
        query = "SELECT * FROM {}".format(admin_base_name)
        sel.execute(query)
        row = sel.fetchone()
        base_auth= basicauth.encode(row[1],row[2])
        if(auth_string==base_auth):
            truncate_conn = sqlite3.connect(base_name)
            sel = truncate_conn.cursor()
            query = "DELETE FROM {}".format(base_name)
            sel.execute(query)
            truncate_conn.commit()
            truncate_conn.close()
            status = True
            return json.dumps({"status":status}),200,{'ContentType':'application/json'}
            
        else:
            auth_conn.close()
            return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}
        
    else:
        return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}