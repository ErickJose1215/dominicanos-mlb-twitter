# fetch_stats.py

from mlbstatsapi import Mlb
from datetime import datetime, timedelta
import pandas as pd
from classify import clasificar_actuacion

DOMINICANOS = [
    "Rafael Devers", "Carlos Santana", "José Ramírez", "Willy Adames",
    "Víctor Robles", "Julio Rodríguez", "Jorge Polanco", "Miguel Andújar",
    "Christopher Morel", "Junior Caminero", "Leody Taveras", "Manny Machado",
    "Fernando Tatis Jr.", "Santiago Espinal", "Elly De La Cruz", "Jeimer Candelario",
    "Jeremy Peña", "Yainer Díaz", "Willi Castro", "Ramón Laureano", "Gary Sánchez",
    "Jorge Mateo", "Vladimir Guerrero Jr.", "Juan Soto", "Mark Vientos",
    "José Siri", "Starling Marte", "Jasson Domínguez", "Austin Wells",
    "Enmanuel Valdez", "Oneil Cruz", "Teoscar Hernández", "Geraldo Perdomo",
    "Luis Garcia Jr."
]

def obtener_actuaciones():
    mlb = Mlb()
    ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    games = mlb.get_schedule(start_date=ayer, end_date=ayer)['dates']
    jugadores_data = []

    for game in games:
        for g in game['games']:
            box = mlb.get_boxscore(game_id=g['gamePk'])
            for team_side in ['home', 'away']:
                for p in box[team_side]['players']:
                    jugador = box[team_side]['players'][p]
                    nombre = jugador['person']['fullName']
                    stats = jugador.get('stats', {}).get('batting', {})

                    if nombre in DOMINICANOS and stats:
                        ab = stats.get('atBats', 0)
                        h = stats.get('hits', 0)
                        hr = stats.get('homeRuns', 0)
                        r = stats.get('runs', 0)
                        rbi = stats.get('rbi', 0)
                        bb = stats.get('baseOnBalls', 0)
                        so = stats.get('strikeOuts', 0)
                        sb = stats.get('stolenBases', 0)
                        doubles = stats.get('doubles', 0)
                        triples = stats.get('triples', 0)

                        clasificacion = clasificar_actuacion(h, hr, r, rbi, bb)

                        jugadores_data.append({
                            "Jugador": nombre,
                            "": clasificacion,
                            "AB": ab,
                            "H": h,
                            "2B": doubles,
                            "3B": triples,
                            "HR": hr,
                            "R": r,
                            "RBI": rbi,
                            "BB": bb,
                            "SO": so,
                            "SB": sb
                        })

    df = pd.DataFrame(jugadores_data)
    df = df.sort_values(by=["", "H", "HR", "RBI"], ascending=[True, False, False, False])
    return df
