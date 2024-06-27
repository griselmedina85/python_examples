import requests
import pandas as pd
import matplotlib.pyplot as plt
from gmplot import gmplot

# URL base de la API
base_url = 'https://apitransporte.buenosaires.gob.ar/ecobici/gbfs/stationInformation'

# Credenciales
client_id = 'fa2dd391243440c0bb5c67adee921817'
client_secret = '0d1bB587EAC345039B1c2Dec89581b00'

# Parámetros de consulta
params = {
    'client_id': client_id,
    'client_secret': client_secret
}

# Hacer la solicitud GET a la API
# response = requests.get(base_url, params=params)
# data = response.json()

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f'Error en la solicitud: {e}')
    exit()

# Verificar el estado de la respuesta
if response.status_code == 200:
    print('Respuesta exitosa:',response.status_code)
else:
    print('Error:', response.status_code)


#añadir try except
# Extraer información relevante
stations = data['data']['stations']

# Crear un DataFrame con los datos extraídos
df_stations = pd.DataFrame(stations)
# print(df_stations.head())

# Seleccionar columnas específicas
df_filtered = df_stations[['station_id', 'name', 'lat', 'lon', 'capacity']]
print(df_filtered.head())


# Gráfico de barras de la capacidad de las estaciones
# plt.figure(figsize=(10, 6))
# plt.bar(df_filtered['name'], df_filtered['capacity'])
# plt.xlabel('Estaciones')
# plt.ylabel('Capacidad')
# plt.title('Capacidad de Estaciones de Ecobici')
# plt.xticks(rotation=90)  # Rotar etiquetas en el eje x para mejor visualización
# plt.show()

# Gráfico de barras de la capacidad de las estaciones
# plt.figure(figsize=(15, 8))  # Aumentar el tamaño de la figura
# plt.bar(df_filtered['name'], df_filtered['capacity'])
# plt.xlabel('Estaciones')
# plt.ylabel('Capacidad')
# plt.title('Capacidad de Estaciones de Ecobici')
# plt.xticks(rotation=90, ha='right')  # Rotar etiquetas y alinearlas a la derecha
# plt.tight_layout()  # Ajustar el espaciado para evitar solapamientos
# plt.show()


# Filtrar las 20 estaciones con mayor capacidad
df_top_stations = df_filtered.nlargest(20, 'capacity')
print(df_top_stations)

# Gráfico de barras de la capacidad de las estaciones
plt.figure(figsize=(15, 8))  # Aumentar el tamaño de la figura
plt.bar(df_top_stations['name'], df_top_stations['capacity'])
plt.xlabel('Estaciones')
plt.ylabel('Capacidad')
plt.title('Top 20 Estaciones de Ecobici por Capacidad')
plt.xticks(rotation=90, ha='right')  # Rotar etiquetas y alinearlas a la derecha
plt.tight_layout()  # Ajustar el espaciado para evitar solapamientos
plt.show()

#AIzaSyCCO6I9dn1uJknxSxb4noVV57ZCq_mSqnY


# Definir la clave de la API de Google Maps
google_maps_api_key = 'AIzaSyCCO6I9dn1uJknxSxb4noVV57ZCq_mSqnY'

# Crear un objeto de gmplot
gmap = gmplot.GoogleMapPlotter(-34.6083, -58.3712, 13, apikey=google_maps_api_key)  # Coordenadas centrales de Buenos Aires

# Añadir marcadores al mapa
for _, row in df_filtered.iterrows():
    gmap.marker(row['lat'], row['lon'], title=row['name'])

# Guardar el mapa en un archivo HTML
gmap.draw('mapa_ecobici.html')

print('Mapa generado: mapa_ecobici.html')


