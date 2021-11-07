import flask
import sqlite3 
import json
import basicauth
from config import base_name
from config import admin_base_name
from config import peek_prefix
from config import db_prefix
from plugins.seleniumplugin import Selenium_Plugin
from plugins.connector import Base_Connector

create_get_api = flask.Blueprint("create_get_api", __name__)

@create_get_api.route("/get")
def get_url():
    headers = flask.request.headers
    auth_string =  headers.get("Authorization")
    if(auth_string is not None):
        b=admin_base_name+db_prefix
        q = "SELECT * FROM {}".format(admin_base_name)
        b_c = Base_Connector(b,q,True,False,False)
        row = b_c.connect_base()
        base_auth= basicauth.encode(row[1],row[2])
        if(auth_string==base_auth):
            prefix = peek_prefix
            passed_url = headers.get("Check-Url").replace(prefix,"").strip()
            if(passed_url is not None):
                b = base_name+db_prefix
                q = "SELECT * FROM {} WHERE urlaskey = '{}'".format(str(base_name),str(passed_url).replace(".html","").strip())
                b_c = Base_Connector(b,q,False,True,False)
                rows = b_c.connect_base()
                length = len(rows)
                message = ""
                if(length==0):
                    message = False
                    if(message==False):
                        passed_url = prefix+passed_url
                        b = base_name+db_prefix
                        sc = Selenium_Plugin(passed_url)
                        soup = sc.selenium_ini()
                        q = "INSERT INTO {} (urlaskey,urlvalue) VALUES ('{}','{}')".format(base_name,str(passed_url).replace(prefix,"").replace(".html","").strip(), soup)
                        b_c = Base_Connector(b,q,False,False,True)
                        b_c.connect_base()
                        return json.dumps({"status":message}),200,{'ContentType':'application/json'}  
                else:
                    b = base_name+db_prefix
                    q = ("SELECT * FROM {} WHERE urlaskey = '{}'").format(base_name,str(passed_url).replace(prefix,"").replace(".html","").strip())
                    b_c = Base_Connector(b,q,False,True,False)
                    rows = b_c.connect_base()
                    message =rows[0][2]
                return json.dumps({"status":message}),200,{'ContentType':'application/json'}  
            else:
                return json.dumps({"status":"You must set an url, bubs"}),200,{'ContentType':'application/json'}     
            
        else:
            return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}
        
    else:
        return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}