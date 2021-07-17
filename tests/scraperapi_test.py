import requests

url = 'http://www.midis101.com/midi_download/49130/DE7C2B86684DF09E527BA893DBFF3280/Italian_883__883_Senzavertiqui'
payload = {'api_key': '6aa20f88f2311b79ae3443c6160293ee', 'url': url, 'keep_headers': True}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip'
}

normal_response = requests.get(url)
proxy_response = requests.get('http://api.scraperapi.com', params=payload, headers=headers)

print(normal_response.content == proxy_response.content)
