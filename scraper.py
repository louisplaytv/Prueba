import requests
from bs4 import BeautifulSoup
import json

def scrape_efootball_real():
    url = "https://www.efootballdb.com/updated-players"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        lista_jugadores = []
        
        # Intentamos buscar cualquier tabla si la clase específica falló
        table = soup.find('table') 
        rows = table.find_all('tr')[1:16] if table else []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                nombre = cols[1].text.strip()
                posicion = cols[2].text.strip()
                media = cols[3].text.strip()
                img = cols[0].find('img')
                foto_url = img.get('data-src') or img.get('src') if img else ""
                
                if foto_url and foto_url.startswith('/'):
                    foto_url = "https://www.efootballdb.com" + foto_url

                lista_jugadores.append({
                    "nombre": nombre,
                    "posicion": posicion,
                    "media": media,
                    "foto": foto_url,
                    "build": {"Tiro": 8, "Pase": 6, "Destreza": 10, "Fuerza": 5} # Build estándar
                })

        # SI EL SCRAPING FALLÓ (lista vacía), creamos datos de prueba para que la web funcione
        if not lista_jugadores:
            return [
                {"nombre": "DATOS EN MANTENIMIENTO", "posicion": "SVR", "media": "99", "foto": "", "build": {"Tiro": 0, "Pase": 0, "Destreza": 0, "Fuerza": 0}}
            ]
            
        return lista_jugadores
    except Exception as e:
        print(f"Error: {e}")
        return []

datos = scrape_efootball_real()
with open('players.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)
