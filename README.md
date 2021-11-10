# Peekaboo

Prerender for ReactJS projects written purely in python (flask). It uses SQlite to store the rendered data.

How did this idea come into my mind? Well, I did not find the tool that suited my personal needs anywhere. So, I created one myself
but it was way more better than I expected it to be. And that's why I decided to share the codebase with you all. Maybe, it will help to boost your
creativity and personal projects, too.

[![wakatime](https://wakatime.com/badge/user/1fbc8005-b2d0-4f4f-93e8-f12d7d25d676/project/6bedca1c-3663-4f94-9501-040e7a50e0d9.svg)](https://wakatime.com/badge/user/1fbc8005-b2d0-4f4f-93e8-f12d7d25d676/project/6bedca1c-3663-4f94-9501-040e7a50e0d9)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K06VU8Z)

# Ingredients

- BeautifulSoup
- Basic Auth
- Requests
- Chromedriver-py
- Flask
- Selenium
- Waitress server
- SQlite
- Isolated Virtual Python Environments
- Lots of Python
- Redis Support (Py-redis)

# Config

## config.py

You have config.py file to make an initial configuration

peekaboo_agent="Peekaboo-Prerender" - Browser user agent

webdriver_path=binary_path - Gets a chrome webdriver path, but you need to install Chrome

peekaboo_admin="test" - username

peekaboo_password="test" - password

peekaboo_ip="127.0.0.1" - Your IP address (external or internal)

peekaboo_port="8000" - Port you're gonna to run the Peekaboo on

peek_prefix="https://" - Changes https:// to ... None, zero, gone or " ". You might want to change it to http://
if you are still running http

# Recommended examplary config settings for now

```

from chromedriver_py import binary_path
base_name="datastore"
admin_base_name="admintable"
peek_prefix="https://"
peekaboo_admin="test"
peekaboo_password="test"
db_prefix=".db"
peekaboo_agent="Peekaboo-Prerender"
webdriver_path=binary_path
peekaboo_ip="127.0.0.1"
peekaboo_port="8000"
eliminate_links = ["script", "iframe","link"] (You can add ,"style", if you want to experiment a little bit)
eliminate_tags = ["class", "id", "name"] (You can add ,"style", if you want to experiment a little bit)
selenium_timeout = 3 (timeout in seconds to wait until the page renders)
helper_route_enabled = True (Set to False to disable)

#Redis
redis_support_enabled = True
redis_host = "localhost"
redis_port = 6379
redis_db = 0

```

# Routes

## peekaboo.py

Greets you with {"Server says": "Peekaboo server is running smoothly..."} message

## ini.py

Visit it once or make a request once to /ini endpoint and you will see {"status": "Data and admin storage created !", "length": 1} message

## helper.py

This endpoint spits out the authorization header needed for auth

Disable helper.py route when you decide to push it to production

(Since 2021-11-08 you can do it programatically)

## truncate.py

Clears the url table completely

## get.py

Checks SQlite database. If url does not exist, Peekaboo scrapes the webpage by url, but spits
{"status":false} JSON message on the first try. It gives back the right data on the second time only.

When it gets the right information, it gives back JSON object also. It looks like:

{"status":"some html to give back"}

You can check SQlite stored data directly like this:

```

sqlite3 datastore.db
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> SELECT urlaskey FROM datastore ORDER BY id ASC limit 10
   ...>
www.artefaktas.eu/
www.artefaktas.eu/2021/11/ar-issprendziau-savo-react-seo-problema
www.artefaktas.eu/2021/10/ar-issprendziau-savo-react-seo-problema
www.artefaktas.eu/2021/10/pssst-nori-parodysiu-kaip-veikia-tikras
www.artefaktas.eu/2021/10/ar-as-susikuriau-tik-tok-react
www.artefaktas.eu/2021/10/bet-react-nepalaiko-twitter-embed
www.artefaktas.eu/2021/10/pora-react-komponentu
www.artefaktas.eu/2021/10/juk-zadejau-nauju-blogger-temu-pirmoji
www.artefaktas.eu/2021/10/cloudflare-cache-api-atsako-antrasciu
www.artefaktas.eu/2021/10/kaip-sukuriau-twitter-siena-savo

```

## update.py

Lets to update the current stored value.

Key value -> url

Data stored -> scraped html

# Ubuntu issues

How the heck do I start a venv in Ubuntu? Welp, look into the folder called linux
and a file called "starter.sh"

## crontab -e

Just an example task if your server shuts down / restarts unexpectedly

SHELL=/bin/bash

@reboot cd /root/flask && ./starter.sh

# If you loose your credentials

... Delete the two databases completely, change your username and password in config.py,
start the venv and visit /ini path once. That is how the databases will recreate.
You will loose the information stored there, but you will regain the access and everything
will work again as expected.

Or... cd into your folder

ls

sqlite3 yourbasename.db and change your username and password directly

# Cloudflare middleware

I used the Cloudflare to check some things here and there to serve generated pages back only to the
crawler bots.

## Middleware script

cloudflaremiddleware.js is somewhere in the root directory of this project

# How do I start venvs manually?

## Windows

cd into the flask directory

```

venv\Scripts\activate
python3 (or just py) peekaboo.py

```

## Linux

cd into flask directory

```

source venv/bin/activate
python3 (or just py) peekaboo.py

```

# How do I... Upload venvs to the remote machine? What about SCP, huh? (Has nothing in common with SCP Foundation)

Turn on the good oldie terminal, cmd, PowerShell or anything that supports scp

```

scp -r C:\Users\arty\Desktop\peekaboo\peekaboo\linux root@ipdaddress:/root/yadayada

write your password, press enter and enjoy the uploading

Putty: pscp -scp

```

# How do I... Make Peekaboo available through HTTPS?

## Apache

```

root@altiusday:~/flask# cd /etc/apache2/sites-available

nano 000-default.conf

<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html/
        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>
<VirtualHost *:443>
    ServerAdmin youremail@domain.lt
    ServerName yourdomain.lt
    ServerAlias www.yourdomain.lt
    DocumentRoot /var/www/html/
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    ProxyRequests On
    ProxyPreserveHost On
    ProxyPass /peekabooproxy/ http://pekabooip:peekabooport/
    ProxyPassReverse /peekabooproxy/ http://pekabooip:peekabooport/
    SSLEngine on
    SSLCertificateFile /root/cloudflare/key.pem
    SSLCertificateKeyFile /root/cloudflare/key.key
</VirtualHost>

```

# How do I... Authenticate myself in, huh? There is a special python file named auth.py dedicated especially for testing purposes

Well...

```

pip install basicauth

import basicauth

peekaboo_admin=hashlib.sha1(str(peekaboo_admin).encode()).hexdigest()
peekaboo_password=hashlib.sha1(str(peekaboo_password).encode()).hexdigest()

encoded_string = basicauth(peekaboo_admin,peekaboo_password)

print(encoded_string)

Try this solution

And please, please, do not forget the headers part

headers={
    "Authorization":"Basic {}".format(encoded_string)
    "Check-Url":str("https://yoursite.domain/page.html").replace(".html","").strip()
}

r = requests.get("http//yourip:yourport/yourendpoint",headers=headers)

Or change the basic request to the best solution that works for you

```

# How do I... Push all the links to Peekaboo?

```
pip install bs4
pip install requests

import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class StaticGen:
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.url_to_get = "https://www.yoursite.eu/sitemap.xml"
        self.rss_array=[]
        self.url_array=[]


    def get_starter(self):
        r = requests.get(self.url_to_get,headers=self.headers)
        soup = BeautifulSoup(r.text,"lxml")
        locs = soup.find_all("loc")
        for loc in locs:
            self.rss_array.append(loc.text)

    def get_urls(self, passed_url):
        d = requests.get(passed_url,headers=self.headers)
        linksoup = BeautifulSoup(d.text,"lxml")
        linklocs = linksoup.find_all("loc")
        for linkloc in linklocs:
            self.url_array.append("{}".format(linkloc.text).replace("http","https"))


    def push_links(self):
        for rss in self.rss_array:
            self.get_urls(rss)

    def links(self):
        for idx, single_url in enumerate(self.url_array):
            headers={
                "Authorization":"Basic yorsecretbase64key186481984126eiuaxsakxjklyadayadayada",
                "Check-Url":str(single_url).strip()
            }
            posturl = "http://yourip:yourport/get"
            r = requests.get(posturl,headers=headers)
            print("Status: {} | Url: {} Left: {}".format(r.status_code, single_url,len(self.url_array)-(idx+1)))

requester = StaticGen()
requester.get_starter()
requester.push_links()
requester.links()

```

# How do I ... Know that Redis is working?

Assuming that you already installed the Redis package, changed your config, restarted the server and made some requests to store the data...

Use Redis CLI to check it out.

KEYS (pattern, you can use an asterisk like I did) - lists all the stored keys

get (keyid) - prints stored key value (in our case HTML)

```

root@altiusday:~# redis-cli
127.0.0.1:6379> KEYS *
1) "www.artefaktas.eu/2021/10/pora-react-komponentu"
2) "www.artefaktas.eu/"
3) "www.artefaktas.eu/2021/11/flask-per-https-ubuntu-apache"
4) "www.artefaktas.eu/2021/11/reikia-programinio-kodo-google"
127.0.0.1:6379> get www.artefaktas.eu/2021/10/pora-react-komponentu

```

# Contacts

andrius@artefaktas.eu

<img src="https://media.giphy.com/media/vzO0Vc8b2VBLi/giphy.gif" height="450" width="100%"/>
