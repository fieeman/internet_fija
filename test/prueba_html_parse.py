import requests_html
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
t0 = time.process_time()


#8990792
# #DE8815@7C3C53*
#PASSWORD = '#78806C@7120C1*'

def wifiNeighbors(request):
    wifi_neighbors = []
    wifi_neighbors_html = request.html.xpath("//div[@class='insighttable table m_box3title']")
    if (len(wifi_neighbors_html) > 0):
        wifi_neighbors_html = wifi_neighbors_html[0].xpath("//div[@class='table-row m_tablebox']")
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
    return wifi_neighbors
def wifiChannels(request):
    wifi_channels_2g_html = request.html.xpath("//div[@class='2gtable table m_box3title']")
    wifi_channels_2g = []
    if (len(wifi_channels_2g_html) > 0):
        wifi_channels_2g_html = wifi_channels_2g_html[0].xpath("//div[@class='table-row m_tablebox']")
        for row in wifi_channels_2g_html:
            channel_info = {}
            temp = row.text.split("\n")
            channel_info['channel'] = temp[1]
            channel_info['devices'] = temp[3]
            channel_info['percent'] = temp[5]
            wifi_channels_2g.append(channel_info)
    wifi_channels_5g_html = request.html.xpath("//div[@class='5gtable table m_box3title']")
    wifi_channels_5g = []
    if (len(wifi_channels_5g_html) > 0):
        wifi_channels_5g_html = wifi_channels_5g_html[0].xpath("//div[@class='table-row m_tablebox']")
        for row in wifi_channels_5g_html:
            channel_info = {}
            temp = row.text.split("\n")
            channel_info['channel'] = temp[1]
            channel_info['devices'] = temp[3]
            channel_info['percent'] = temp[5]
            wifi_channels_5g.append(channel_info)
    return {"2g": wifi_channels_2g,"5g": wifi_channels_5g}

def statusModem(session,headers):
    r = session.get("https://192.168.1.165/Status.asp",headers=headers,verify=False)
    r.html.render()
    status = {}
    status_html = r.html.xpath("//div[@class='h3-content']")
    if (len(status_html) > 0):
        status_html = status_html[0].xpath("//div[@class='row']")
        for row in status_html:
            temp = row.text.split("\n")
            status[temp[0]] = temp[1]
        traffic_info_html = r.html.xpath("//div[@class='h3-content no-padding-bottom']")
        if (len(traffic_info_html) > 0):
            traffic_info_html = traffic_info_html[2].xpath("//div[@class='row']")
            for row in traffic_info_html:
                temp = row.text.split("\n")
                if (temp[0] != temp[-1]):
                    status[temp[0]] = temp[-1]
                else:
                    status[temp[0]] = "null"
    return status

def currentInfo(session,headers):
    current_info = {}
    r = session.get('https://192.168.1.165/WifiGeneral.asp',headers=headers,verify=False)
    r.html.render()
    current_info_2g_html = r.html.xpath("//div[@class='h3-content clearfix no-padding-bottom wifiOnOff']")
    if (len(current_info_2g_html) > 0):
        current_info_2g_html = current_info_2g_html[0].xpath("//div[@class='row']")
        temp1 = current_info_2g_html[0].text.split("\n")
        temp2 = current_info_2g_html[1].text.split("\n")
        current_info['2g'] = {
            temp1[0] : temp1[1],
            temp2[0] : temp2[1]
        }
    current_info_5g_html = r.html.xpath("//div[@class='h3-content clearfix no-padding-bottom wifi5GOnOff']")
    if (len(current_info_5g_html) > 0):
        current_info_5g_html = current_info_5g_html[0].xpath("//div[@class='row']")
        temp1 = current_info_5g_html[0].text.split("\n")
        temp2 = current_info_5g_html[1].text.split("\n")
        current_info['5g'] = {
            temp1[0] : temp1[-1],
            temp2[0] : temp2[-1]
        }
    return current_info

def clientsWifi(session,headers):
    r = session.get("https://192.168.1.165/WifiClients.asp",headers=headers,verify=False)
    r.html.render() #table-row m_tablebox 2gtable m_box3title
    clients_html = r.html.xpath("//div[@class='2gtable m_box3title']")
    clientes_2g = []
    clientes_5g = []
    clientes = {}
    if (len(clients_html) > 0):
        clients_html = clients_html[0].xpath("//div[@class='table-row m_tablebox']")
        for c in clients_html:
            client = {}
            temp = c.text.split("\n")
            client[temp[0]] = temp[1]
            client[temp[2]] = temp[3]
            client[temp[4]] = temp[5]
            client[temp[6]] = temp[7]
            client[temp[8]] = temp[9]
            client[temp[10]] = temp[11]
            client[temp[12]] = temp[13]
            clientes_2g.append(client)
    clientes['2g'] = clientes_2g

    clients_html = r.html.xpath("//div[@class='5gtable m_box3title']")
    if (len(clients_html) > 0):
        clients_html = clients_html[0].xpath("//div[@class='table-row m_tablebox']")
        for c in clients_html:
            client = {}
            temp = c.text.split("\n")
            client[temp[0]] = temp[1]
            client[temp[2]] = temp[3]
            client[temp[4]] = temp[5]
            client[temp[6]] = temp[7]
            client[temp[8]] = temp[9]
            client[temp[10]] = temp[11]
            client[temp[12]] = temp[13]
            clientes_5g.append(client)
    clientes['5g'] = clientes_5g
    return clientes



@profile
def main():
    POST_LOGIN_URL = 'https://192.168.1.165/goform/AskLogin'
    PASSWORD = 'Diciembre2018+'
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
    for i in range(10):
        
        with requests_html.HTMLSession(verify=False) as session:
            
            print("Login")
            r = session.post(POST_LOGIN_URL,data=payload,headers=headers,verify=False)
            print(r.status_code)
            print("Navegacion")

            r = session.get("https://192.168.1.165/WifiInsight.asp",headers=headers,verify=False)
            r.html.render()
            print("Wifi Neighbros")
            wifi_neighbors = wifiNeighbors(r)
            print("Wifi Channels")
            wifi_channels = wifiChannels(r)
            wifi_channels_2g = wifi_channels["2g"]
            wifi_channels_5g = wifi_channels["5g"]
            print("Wifi current State")
            current_wifi_info = currentInfo(session,headers)
            print("Wifi Clients")
            clients_wifi = clientsWifi(session,headers)
            print("Status Modem")
            status_modem = statusModem(session,headers)
            modem_askey = {}
            modem_askey['neighbors'] = wifi_neighbors
            modem_askey['wifi_channels_2g'] = wifi_channels_2g
            modem_askey['wifi_channels_5g'] = wifi_channels_5g
            modem_askey['current_wifi_info'] = current_wifi_info
            modem_askey['clients_wifi'] = clients_wifi
            modem_askey['status_modem'] = status_modem
            print(json.dumps(modem_askey,indent=4))
            #https://192.168.1.165/WifiClients.asp

    

if __name__ == '__main__':
    main()
    print(time.process_time() - t0)