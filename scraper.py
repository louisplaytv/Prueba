import requests
from bs4 import BeautifulSoup
import json

def generar_build_pro(posicion):
    # Lógica de entrenamiento optimizada tipo HUB
    builds = {
        "CF": {"Tiro": 10, "Pase": 0, "Destreza": 12, "Fuerza": 8},
        "RWF": {"Tiro": 8, "Pase": 6, "Destreza": 12, "Fuerza": 4},
        "LWF": {"Tiro": 8, "Pase": 6, "Destreza": 12, "Fuerza": 4},
        "AMF": {"Tiro": 6, "Pase": 10, "Destreza": 8, "Fuerza": 4},
        "CB": {"Tiro": 0, "Pase": 2, "Destreza": 4, "Fuerza": 12},
        "GK": {"Tiro": 0, "Pase": 0, "Destreza": 0, "Fuerza": 0}
    }
    return builds.get(posicion, {"Tiro": 5, "Pase": 5, "Destreza": 5, "Fuerza": 5})

def scrape_top_players():
    # Cambiamos la URL a la lista de jugadores con mejor media
    url = "https://www.efootballdb.com/players?sort=overall_max&order=desc"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        jugadores = []
        
        # Buscamos las filas de la tabla
        rows = soup.select('table.table-sorted tr')[1:31] # Traemos los mejores 30
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 4:
                nombre = cols[1].text.strip()
                posicion = cols[2].text.strip()
                media = cols[3].text.strip()
                
                # Extraer foto
                img = cols[0].find('img')
                foto_url = img.get('data-src') or img.get('src') if img else ""
                if foto_url and foto_url.startswith('/'):
                    foto_url = "https://www.efootballdb.com" + foto_url

                jugadores.append({
                    "nombre": nombre,
                    "posicion": posicion,
                    "media": media,
                    "foto": foto_url,
