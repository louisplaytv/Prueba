import requests
from bs4 import BeautifulSoup
import json

def generar_build_pro(posicion):
    builds = {
        "CF": {"Tiro": 10, "Pase": 0, "Destreza": 12, "Fuerza": 8},
        "RWF": {"Tiro": 8, "Pase": 6, "Destreza": 12, "Fuerza": 4},
        "LWF": {"Tiro": 8, "Pase": 6, "Destreza": 12, "Fuerza": 4},
        "AMF": {"Tiro": 6, "Pase": 10, "Destreza": 8, "Fuerza": 4},
        "CB": {"Tiro": 0, "Pase": 2, "Destreza": 4, "Fuerza": 12},
        "GK": {"Tiro": 0, "Pase": 0, "Destreza": 0, "Fuerza": 0}
    }
    return builds.get(posicion, {"Tiro": 4, "Pase": 4, "Destreza": 4, "Fuerza": 4})

def scrape_top_players():
    url = "https://www.efootballdb.com/players?sort=overall_max&order=desc"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        jugadores = []
        
        table = soup.find('table')
        if not table:
            return []

        rows = table.find_all('tr')[1:31] # Traemos los mejores 30
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 4:
                nombre = cols[1].text.strip()
                posicion = cols[2].text.strip()
                media = cols[3].text.strip()
                
                img = cols[0].find('img')
                foto_url = img.get('data-src') or img.get('src') if img else ""
                if foto_url and foto_url.startswith('/'):
                    foto_url = "https://www.efootballdb.com" + foto_url

                jugadores.append({
                    "nombre": nombre,
                    "posicion": posicion,
                    "media": media,
                    "foto": foto_url,
                    "build": generar_build_pro(posicion)
                })
        return jugadores
    except Exception as e:
        print(f"Error en el scraping: {e}")
        return []

# Ejecución principal
if __name__ == "__main__":
    datos = scrape_top_players()
    with open('players.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"¡Hecho! Guardados {len(datos)} jugadores.")
