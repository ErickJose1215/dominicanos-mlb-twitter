from pybaseball import statcast
import pandas as pd
from datetime import datetime, timedelta

# Lista fija de jugadores dominicanos (puedes extenderla)
DOMINICAN_PLAYERS = [
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

def get_performances():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    data = statcast(start_dt=yesterday, end_dt=yesterday)

    if data.empty:
        return pd.DataFrame()

    # Filtrar solo apariciones de bateo
    batting_data = data[data['description'].notnull()]
    
    # Agrupar por jugador
    summary = (
        batting_data.groupby("player_name")
        .agg({
            "events": lambda x: list(x),
            "description": "count"
        })
        .reset_index()
    )

    players = []

    for _, row in summary.iterrows():
        name = row["player_name"]
        if name not in DOMINICAN_PLAYERS:
            continue

        events = row["events"]
        ab = len(events)
        h = sum(1 for e in events if e in ["single", "double", "triple", "home_run"])
        hr = events.count("home_run")
        bb = events.count("walk") + events.count("intent_walk") + events.count("hit_by_pitch")
        so = events.count("strikeout")
        rbi = 0  # No incluido directamente en Statcast
        sb = 0   # Tampoco directamente, puedes integrar otra fuente si quieres
        r = 0    # No disponible en este nivel

        players.append({
            "Player": name,
            "AB": ab,
            "H": h,
            "2B": events.count("double"),
            "3B": events.count("triple"),
            "HR": hr,
            "R": r,
            "RBI": rbi,
            "BB": bb,
            "SO": so,
            "SB": sb
        })

    df = pd.DataFrame(players)
    return df
