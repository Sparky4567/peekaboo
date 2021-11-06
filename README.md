# Peekaboo

Peekaboo prerender for reactjs projects written purely in python (flask)

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

# Recommended exmplary config settings for now

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

```

# Routes

## helper.py

This endpoint spits out the authorization header needed for auth
Disable helper.py routes when you decide to push it to production

## truncate.py

Clears the url table

## get.py

Checks sqlite database if url already exists, if not, Peekaboo scrapes the webpage by url, but spits
{"status":false} JSON message. It gives back the right data from the second time only.

When it gets the right information, it gives back JSON object also. It looks like:

{"status":"some html to give back"}

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
venv\Scripts\activate
python3 (or just py) peekaboo.py

## Linux

cd into flask directory
source venv/bin/activate
python3 (or just py) peekaboo.py

# How do I... Authenticate myself in, huh?

Well...

```

pip install basicauth

import basicauth

encoded_string = basicauth(username,password)

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
                "Check-Url":str(single_url).replace(".html","").strip()
            }
            posturl = "http://yourip:yourport/get"
            r = requests.get(posturl,headers=headers)
            print("Status: {} | Url: {} Left: {}".format(r.status_code, single_url,len(self.url_array)-(idx+1)))

requester = StaticGen()
requester.get_starter()
requester.push_links()
requester.links()

```

# Contacts

andrius@artefaktas.eu
