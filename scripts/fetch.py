#!/usr/bin/env python3

import requests
import pandas as pd

df = pd.read_csv('presidente.csv')
data = requests.post('https://computo.oep.org.bo/api/v1/resultado/presidente').json()
newrow = {partido['nombre']: partido['valor'] for partido in data['datoAdicional']['grafica']}
newrow['tiempo'] = data['fecha']
df.append(newrow, ignore_index=True).to_csv('presidente.csv', index=False)
