from pybaseball import statcast_batter, playerid_lookup
import pandas as pd

# Paso 1: Buscar el ID de Juan Soto
soto_info = playerid_lookup("soto", "juan")
soto_id = soto_info.loc[0, "key_mlbam"]

print(f"📌 ID de Juan Soto: {soto_id}")

# Paso 2: Descargar data de Statcast para ese día
df = statcast_batter("2025-04-07", "2025-04-07", soto_id)

if df.empty:
    print("❌ Juan Soto no tuvo actividad ofensiva ese día.")
else:
    print(f"✅ {len(df)} lanzamientos registrados para Juan Soto.")

    # Paso 3: Seleccionar columnas clave para análisis
    columnas = [
        'game_date', 'at_bat_number', 'pitch_type', 'release_speed',
        'player_name', 'description', 'events', 'bb_type',
        'balls', 'strikes', 'bat_score', 'hit_location'
    ]

    df_filtrado = df[columnas].sort_values(by=['at_bat_number', 'game_date'])

    # Paso 4: Mostrar resultados
    pd.set_option("display.max_rows", None)  # Muestra todo sin cortar
    print("\n🧾 Detalles de cada pitcheo:")
    print(df_filtrado)
