import requests

url = 'http://www.midis101.com/midi_download/49130/DE7C2B86684DF09E527BA893DBFF3280/Italian_883__883_Senzavertiqui'
payload = {'api_key': '6aa20f88f2311b79ae3443c6160293ee', 'url': url}

normal_response = requests.get(url)
proxy_response = requests.get('http://api.scraperapi.com', params=payload)

print(normal_response.content == proxy_response.content)
