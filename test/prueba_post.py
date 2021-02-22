import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

POST_LOGIN_URL = 'https://192.168.1.165/goform/AskLogin'
NAME_INPUT = 'Password'
#8990792
# #DE8815@7C3C53*
#PASSWORD = '#78806C@7120C1*'
PASSWORD = 'Diciembre2018+'
REQUEST_URL = 'https://192.168.1.165/WifiGeneral.asp'
payload = {
    'AskUsername': 'admin',
    'AskPassword': PASSWORD
}
headers = {
    "Content-type" : "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}
with requests.Session() as session:
    print("Login")
    post = session.post(POST_LOGIN_URL, data=payload,headers=headers,verify=False)
    print("Navegacion")
    r = session.get(REQUEST_URL,headers=headers,verify=False)
    print(r.content.decode())   #or whatever else you want to do with the request data!
