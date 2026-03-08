import requests
from bs4 import BeautifulSoup
import json

def generar_build_auto(posicion):
    # Lógica simplificada de entrenamiento por posición
    builds = {
        "CF": {"Tiro": 12, "Pase": 0, "Destreza": 8, "Fuerza": 4},
        "SS": {"Tiro": 8, "Pase": 4, "Destreza": 10, "Fuerza": 4},
        "AMF": {"Tiro": 4, "Pase": 10, "Destreza": 8, "Fuerza": 2},
        "CB": {"Tiro": 0, "Pase": 2, "Destreza": 4, "Fuerza": 12},
        "GK": {"Tiro": 0, "Pase": 0, "Destreza": 0, "Fuerza": 0} # El portero lleva otra lógica
    }
    return builds.get(posicion, {"Tiro": 4, "Pase": 4, "Destreza": 4, "Fuerza": 4})

def scrape_efootball():
    url = "https://www.efootballdb.com/updated-players"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lista_jugadores = []
    
    # Buscamos las filas de la tabla de jugadores
    # Nota: Estas clases CSS pueden variar, es la parte que debes vigilar
    rows = soup.find_all('tr')[1:11] # Tomamos los primeros 10 para empezar
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            nombre = cols[1].text.strip()
            posicion = cols[2].text.strip()
            media = cols[3].text.strip()
            
            player_data = {
                "nombre": nombre,
                "posicion": posicion,
                "media": media,
                "build": generar_build_auto(posicion)
            }
            lista_jugadores.append(player_data)
            
    return lista_jugadores

# Guardar en el JSON que lee tu web
datos = scrape_efootball()
with open('players.json', 'w') as f:
    json.dump(datos, f, indent=4)

print(f"¡Éxito! Se han actualizado {len(datos)} jugadores.")
