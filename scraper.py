import json

# Aquí iría la lógica de Scraping (BeautifulSoup), pero para empezar
# este script generará datos de prueba que tú luego puedes conectar
nuevos_jugadores = [
    {"nombre": "L. MESSI", "media": "102", "posicion": "EDD", "build": {"Tiro": 10, "Pase": 8, "Destreza": 12, "Fuerza": 4}},
    {"nombre": "K. MBAPPÉ", "media": "101", "posicion": "DC", "build": {"Tiro": 12, "Pase": 4, "Destreza": 10, "Fuerza": 8}}
]

with open('players.json', 'w') as f:
    json.dump(nuevos_jugadores, f, indent=4)

print("Datos actualizados correctamente.")
