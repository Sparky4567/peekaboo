from flask import Flask
import json
from ini import create_table_api
from helper import create_helper_api
from get import create_get_api
from truncate import create_truncate_api
from waitress import serve
from config import peekaboo_ip
from config import peekaboo_port

app = Flask(__name__)
app.register_blueprint(create_table_api)
app.register_blueprint(create_helper_api)
app.register_blueprint(create_get_api)
app.register_blueprint(create_truncate_api)

@app.route("/peekaboo")
def starter():
    server_string="Server says"
    server_says = "Peekaboo server is running smoothly..."
    return json.dumps({server_string:server_says}),200,{'ContentType':'application/json'}


if __name__ == "__main__":
    print("Waitress is serving...")
    #app.run(host='0.0.0.0')
    serve(app, host=peekaboo_ip, port=peekaboo_port, url_scheme='https')
