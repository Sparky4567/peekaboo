import flask
import sqlite3 
import json
import basicauth
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import base_name
from config import admin_base_name
from config import peek_prefix
from config import peekaboo_agent
from config import webdriver_path
from config import db_prefix
from config import eliminate_links
from config import eliminate_tags
from config import selenium_timeout

create_update_api = flask.Blueprint("create_update_api", __name__)

@create_update_api.route("/update")
def get_url():
    headers = flask.request.headers
    auth_string =  headers.get("Authorization")
    if(auth_string is not None):
        auth_conn = sqlite3.connect(admin_base_name+db_prefix)
        sel = auth_conn.cursor()
        query = "SELECT * FROM {}".format(admin_base_name)
        sel.execute(query)
        row = sel.fetchone()
        base_auth= basicauth.encode(row[1],row[2])
        if(auth_string==base_auth):
            prefix = peek_prefix
            passed_url = headers.get("Check-Url").replace(prefix,"").strip()
            if(passed_url is not None):
                data_conn = sqlite3.connect(base_name+db_prefix)
                sel = data_conn.cursor()
                query = "SELECT * FROM {} WHERE urlaskey = '{}'".format(str(base_name),str(passed_url).replace(".html","").strip())
                sel.execute(query)
                rows = sel.fetchall()
                length = len(rows)
                message = ""
                if(length==1):
                    message = True
                    if(message==True):
                        auth_conn.close()
                        agent = {
                            "User-Agent":peekaboo_agent
                        }
                        weboptions = Options()
                        weboptions.add_argument("user-agent=[{}]".format(agent))
                        weboptions.add_argument("--headless")
                        weboptions.add_argument("--no-sandbox")
                        driver_path = webdriver_path
                        driver = webdriver.Chrome(driver_path,options=weboptions)
                        passed_url = prefix+passed_url
                        driver.get(passed_url)
                        time.sleep(selenium_timeout)
                        insert_conn = sqlite3.connect(base_name+db_prefix)
                        sel = insert_conn.cursor()
                        content = driver.page_source
                        soup = BeautifulSoup(content, 'html.parser')
                        for script in soup(eliminate_links):
                            script.extract()
                        for tag in soup():
                            for attribute in eliminate_tags:
                                del tag[attribute]
                        soup = str(soup).replace('&gt;','>').replace('&lt;','<').replace("'",'"')
                        driver.close()
                        insert_query = "UPDATE {} SET urlvalue='{}' WHERE urlaskey='{}'".format(base_name, soup, str(passed_url).replace(prefix,"").replace(".html","").strip())
                        sel.execute(insert_query)
                        insert_conn.commit()
                        insert_conn.close()
                        message = "Inserted"
                        return json.dumps({"status":message}),200,{'ContentType':'application/json'}  
                else:
                    auth_conn.close()
                    message = "Insert error !"
                return json.dumps({"status":message}),200,{'ContentType':'application/json'}  
            else:
                return json.dumps({"status":"You must set an url, bubs"}),200,{'ContentType':'application/json'}     
            
        else:
            auth_conn.close()
            return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}
        
    else:
        return json.dumps({"status":"Not authorized"}),200,{'ContentType':'application/json'}