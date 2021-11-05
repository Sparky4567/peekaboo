import requests
import basicauth
import requests
headers = basicauth.encode("artefaktas","generator")
headers_to_pass = {
    "Authorization":headers,
    "Check-Url":"https://www.artefaktas.eu"
}
print(headers)
r = requests.get("http://127.0.0.1:5000/get",headers=headers_to_pass)
print(r.text)