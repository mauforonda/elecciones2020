#!/usr/bin/env python3

import requests
import pandas as pd
import csv

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
}

data = '{"tipoArchivo":"CSV"}'

meta = requests.post('https://computo.oep.org.bo/api/v1/descargar', headers=headers, data=data)
response = requests.get(meta.json()['datoAdicional']['archivo'])
csvdata = csv.reader(response.content.decode('iso8859').splitlines(), delimiter=',')

data = []
for row in csvdata:
    if len(row) == 40:
        data.append(row)
    else:
        data.append(row[:15] + [ ''.join(row[15:16+(len(row)-40)]) ] + row[16+(len(row)-40):])

df = pd.DataFrame(data[1:], columns=data[0])
df['RECINTO'] = df.RECINTO.str.replace('[`"\']', '')
filename = 'datos/{}.csv'.format('_'.join(meta.json()['datoAdicional']['archivo'].split('/')[-1].split('_')[1:3]))
df.to_csv(filename, index=False, encoding='utf-8')
