import requests_html
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#8990792
# #DE8815@7C3C53*
#PASSWORD = '#78806C@7120C1*'
POST_LOGIN_URL = 'https://192.168.1.165/goform/AskLogin'
PASSWORD = 'Diciembre2018+'
REQUEST_URL = 'https://192.168.1.165/WifiInsight.asp'
payload = {
    'AskUsername': 'admin',
    'AskPassword': PASSWORD
}
headers = {
    "Content-type" : "application/json",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer" : "https://192.168.1.165/overview.asp",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}

with requests_html.HTMLSession(verify=False) as session:
    print("Login")
    r = session.post(POST_LOGIN_URL,data=payload,headers=headers,verify=False)
    print("Navegacion")
    r = session.get(REQUEST_URL,headers=headers,verify=False)
    print('Renderizando')
    r.html.render()
    print('Renderizado')
    wifi_neighbors = []
    wifi_neighbors_html = r.html.xpath("//div[@class='insighttable table m_box3title']")[0].xpath("//div[@class='table-row m_tablebox']")
    for row in wifi_neighbors_html:
        try:
            data = {}
            temp = row.text.split('\n')
            data['network_name'] = temp[1]
            data['mac'] = temp[3]
            data['channel'] = temp[6]
            data['bw'] = temp[8][:2]
            data['rssi'] = temp[10]
            data['security'] = temp[12]
            wifi_neighbors.append(data)
        except:
            pass
    wifi_channels_2g_html = r.html.xpath("//div[@class='2gtable table m_box3title']")[0].xpath("//div[@class='table-row m_tablebox']")
    wifi_channels_2g = []
    for row in wifi_channels_2g_html:
        channel_info = {}
        temp = row.text.split("\n")
        channel_info['channel'] = temp[1]
        channel_info['devices'] = temp[3]
        channel_info['percent'] = temp[5]
        wifi_channels_2g.append(channel_info)
    wifi_channels_5g_html = r.html.xpath("//div[@class='5gtable table m_box3title']")[0].xpath("//div[@class='table-row m_tablebox']")
    wifi_channels_5g = []
    for row in wifi_channels_5g_html:
        channel_info = {}
        temp = row.text.split("\n")
        channel_info['channel'] = temp[1]
        channel_info['devices'] = temp[3]
        channel_info['percent'] = temp[5]
        wifi_channels_5g.append(channel_info)
    modem_askey = {}
    modem_askey['neighbors'] = wifi_neighbors
    modem_askey['wifi_channels_2g'] = wifi_channels_2g
    modem_askey['wifi_channels_5g'] = wifi_channels_5g

    



    r = session.get('https://192.168.1.165/Status.asp',headers=headers,verify=False)
    print('Renderizando')
    r.html.render()
    print('Renderizado')
    status_html = r.html.xpath("//div[@class='h3-content']")[0].xpath("//div[@class='row']")
    status = {}
    for row in status_html:
        temp = row.text.split("\n")
        status[temp[0]] = temp[1]
    print(json.dumps(status,indent=4))

