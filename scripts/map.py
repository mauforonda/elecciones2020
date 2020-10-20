#!/usr/bin/env python3

import pandas as pd
import os
import folium
import matplotlib
import matplotlib.pyplot as plt
import math

locations = pd.concat([pd.read_excel('scripts/2020_geo_padron_final.xlsx', sheet_name=i)[['Recinto', 'latitud', 'longitud', 'Mesas', 'Habilitados', 'idloc', 'RECI']] for i in [0,1]], axis=0)
locations.index = (locations.idloc.astype(str) + locations.RECI.astype(str)).astype(int)
locations = locations[locations.columns[:5]]
locations.columns = ['recinto', 'latitud', 'longitud', 'mesas', 'habilitados']

votos = pd.read_csv('datos/'+sorted(os.listdir('datos'))[-1])
votos = votos[votos.CANDIDATURA == 'PRESIDENTE']
votos = votos[['ID_LOCALIDAD', 'ID_RECINTO', 'INSCRITOS_HABILITADOS', 'CREEMOS', 'ADN', 'MAS_IPSP', 'FPV', 'PAN_BOL', 'LIBRE_21', 'CC', 'JUNTOS', 'VOTO_VALIDO', 'VOTO_BLANCO', 'VOTO_NULO', 'VOTO_EMITIDO', 'VOTO_VALIDO_SISTEMA', 'VOTO_EMITIDO_SISTEMA']]
votos['id'] = (votos.ID_LOCALIDAD.astype(str) + votos.ID_RECINTO.astype(str)).astype(int)
votos = votos.drop(columns = ['ID_LOCALIDAD', 'ID_RECINTO'])
votos = votos.groupby('id').sum()

df = pd.concat([locations, votos], axis=1).dropna()

cmap = plt.cm.get_cmap('RdYlBu')
df['VOTO_VALIDO'] = df['VOTO_VALIDO'].astype(int)
df['mas_p'] = df['MAS_IPSP'] / df['VOTO_VALIDO']
df['cc_p'] = df['CC'] / df['VOTO_VALIDO']
df['diff'] = df['mas_p'] - df['cc_p']
df['color'] = df.apply(lambda row: matplotlib.colors.rgb2hex(cmap((row['diff'] + 1) / 2)[:3]), axis=1)
df['size'] = df.VOTO_VALIDO.apply(lambda row: math.log(row) if row > 0 else 1)
df['recinto'] = df['recinto'].str.replace('`','')

folium_map = folium.Map(location = [-16.2980907,-58.462965],
                        zoom_start = 4,
                        tiles = "https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",
                        attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')

for row in df.to_dict(orient='records'):
    folium.CircleMarker(location=[row['latitud'], row['longitud']],
                        stroke = False,
                        fill_opacity = .8,
                        radius = row['size'],
                        popup = '<div style="min-width:130px"><p style="margin:5px 0px"><strong>Recinto</strong>: {}</p><p style="margin:5px 0px"><strong>Votos Válidos</strong>: {}</p><p style="margin:5px 0px"><strong>MAS-IPSP</strong>: {:.0%}</p><p style="margin:5px 0px"><strong>CC</strong>: {:.0%}</p></div>'.format(row['recinto'], row['VOTO_VALIDO'], row['mas_p'], row['cc_p']),
                        fill_color=row['color']).add_to(folium_map)

folium_map.save('docs/index.html')
