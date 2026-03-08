import requests
from bs4 import BeautifulSoup
import json

# Imagen por defecto si no se encuentra la del jugador
FOTO_POR_DEFECTO = "https://www.konami.com/efootball/s/img/common/noimage_player.png"

def generar_build_auto(posicion):
    """Fórmula de entrenamiento meta según posición"""
    builds = {
        "CF": {"Tiro": 10, "Pase": 2, "Destreza": 12, "Fuerza": 8}, # Delantero
        "LW": {"Tiro": 8, "Pase": 4, "Destreza": 12, "Fuerza": 6},  # Extremo
        "RW": {"Tiro": 8, "Pase": 4, "Destreza": 12, "Fuerza": 6},
        "AMF": {"Tiro": 6, "Pase": 10, "Destreza": 8, "Fuerza": 4}, # Media Punta
        "CMF": {"Tiro": 4, "Pase": 10, "Destreza": 6, "Fuerza": 6}, # Medio Centro
        "DMF": {"Tiro": 2, "Pase": 8, "Destreza": 4, "Fuerza": 10}, # Pivote
        "CB": {"Tiro": 0, "Pase": 4, "Destreza": 4, "Fuerza": 12},  # Central
        "LB": {"Tiro": 0, "Pase": 6, "Destreza": 8, "Fuerza": 10}, # Lateral
        "RB": {"Tiro": 0, "Pase": 6, "Destreza": 8, "Fuerza": 10},
        "GK": {"Tiro": 0, "Pase": 0, "Destreza": 0, "Fuerza": 0}    # Portero (requiere otra lógica)
    }
    # Si no encuentra la posición exacta, da una genérica equilibrada
    return builds.get(posicion, {"Tiro": 4, "Pase": 4, "Destreza": 4, "Fuerza": 4})

def scrape_efootball_real():
    url = "https://www.efootballdb.com/updated-players"
    # User-Agent para que el sitio crea que somos un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print("Iniciando scraping de eFootballDB...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error accediendo a la web: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    lista_jugadores = []
    
    # Buscamos las filas de la tabla de jugadores
    # NOTA: Estas clases CSS son críticas, si cambian en la web, el scraper falla.
    # Buscamos la tabla con clase 'table-sorted' y luego sus filas 'tr'
    table = soup.find('table', class_='table-sorted')
    if not table:
        print("No se encontró la tabla de jugadores.")
        return []

    rows = table.find_all('tr')[1:21] # Tomamos los primeros 20 jugadores
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 4:
            # --- Extracción de Datos ---
            
            # 1. Nombre
            nombre = cols[1].find('a').text.strip() if cols[1].find('a') else cols[1].text.strip()
            
            # 2. Posición
            posicion = cols[2].text.strip()
            
            # 3. Media (Rating)
            media = cols[3].text.strip()
            
            # 4. FOTO (Nuevo)
            # Buscamos la etiqueta 'img' dentro de la primera columna (td)
            img_tag = cols[0].find('img')
            if img_tag:
                # La mayoría de webs usan 'src' o 'data-src' para carga perezosa
                foto_url = img_tag.get('data-src') or img_tag.get('src')
                # A veces la URL es relativa (/img/...), la convertimos en absoluta
                if foto_url and foto_url.startswith('/'):
                    foto_url = "https://www.efootballdb.com" + foto_url
            else:
                foto_url = FOTO_POR_DEFECTO

            # --- Generación de Datos ---
            player_data = {
                "nombre": nombre,
                "posicion": posicion,
                "media": media,
                "foto": foto_url,
                "build": generar_build_auto(posicion)
            }
            lista_jugadores.append(player_data)
            print(f"Jugador procesado: {nombre} ({posicion})")
            
    return lista_jugadores

# --- Ejecución y Guardado ---
try:
    datos = scrape_efootball_real()
    if datos:
        with open('players.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        print(f"¡Éxito! Se han actualizado {len(datos)} jugadores con fotos en 'players.json'.")
    else:
        print("No se obtuvieron datos.")
except Exception as e:
    print(f"Ocurrió un error general: {e}")
