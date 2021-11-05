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

# Contacts

andrius@artefaktas.eu
