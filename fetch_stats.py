from pybaseball import statcast
import pandas as pd
from datetime import datetime, timedelta

def get_performances():
    # Fecha de ayer
    date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"📅 Extrayendo datos Statcast para el {date}")

    try:
        data = statcast(start_dt=date, end_dt=date)
    except Exception as e:
        print(f"❌ Error al consultar Statcast: {e}")
        return pd.DataFrame()

    if data.empty:
        print("⚠️ Statcast no devolvió datos.")
        return pd.DataFrame()

    # ✅ Tomar solo eventos donde haya un bateador identificado
    batting_data = data[
        data['batter'].notnull() &
        data['player_name'].notnull() &
        data['description'].notnull()
    ]

    print(f"✅ {len(batting_data)} eventos de bateo brutos encontrados.")

    resumen = (
        batting_data.groupby("batter")
        .agg({
            "player_name": "first",
            "events": lambda x: list(x)
        })
        .reset_index()
    )

    jugadores = []
    for _, row in resumen.iterrows():
        name = row["player_name"]
        events = row["events"]

        ab = len(events)
        h = sum(1 for e in events if e in ["single", "double", "triple", "home_run"])
        hr = events.count("home_run")
        bb = events.count("walk") + events.count("intent_walk") + events.count("hit_by_pitch")
        so = events.count("strikeout")

        # Solo incluir jugadores que hayan hecho algo real
        if ab < 1 and h == 0 and hr == 0 and bb == 0:
            continue

        jugadores.append({
            "Player": name,
            "AB": ab,
            "H": h,
            "2B": events.count("double"),
            "3B": events.count("triple"),
            "HR": hr,
            "R": 0,      # No disponible en Statcast
            "RBI": 0,    # No disponible en Statcast
            "BB": bb,
            "SO": so,
            "SB": 0      # No disponible en Statcast
        })

    df = pd.DataFrame(jugadores)

    if df.empty:
        print("⚠️ No se encontraron bateadores con producción real.")
        return df

    print(f"✅ {len(df)} bateadores activos con stats ofensivos.")
    return df.sort_values(by=["H", "HR", "BB"], ascending=False).reset_index(drop=True)
