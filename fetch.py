#!/usr/bin/env python3

import requests
import pandas as pd
from datetime import datetime

headers = {
    'authority': 'computo.oep.org.bo',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'dnt': '1',
    'captcha': 'nocaptcha',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://computo.oep.org.bo',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://computo.oep.org.bo/',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'cookie': '__cfduid=daa9ab4af80430da5e8335616a1d7b9001601047805',
}

data = '{"tipoArchivo":"CSV"}'

response = requests.post('https://computo.oep.org.bo/api/v1/descargar', headers=headers, data=data)

df = pd.read_csv(response.json()['datoAdicional']['archivo'], encoding='iso-8859-1')
filename = datetime.strptime(response.json()['datoAdicional']['fecha'], '%d/%m/%Y %H:%M:%S').strftime('datos/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv(filename, index=False, encoding='utf-8')
