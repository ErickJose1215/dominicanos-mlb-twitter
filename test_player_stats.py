
from pybaseball import batting_stats_range
import pandas as pd

# Nombre del jugador
nombre = "Juan Soto"
fecha_inicio = "2025-04-01"
fecha_fin = "2025-04-08"

# Descargar estadísticas de bateo de Baseball Reference
print(f"📅 Extrayendo datos de Baseball Reference para {nombre} entre {fecha_inicio} y {fecha_fin}...")
df = batting_stats_range(fecha_inicio, fecha_fin)

# Filtrar por el nombre del jugador exacto
df_jugador = df[df['Name'] == nombre]

if df_jugador.empty:
    print(f"❌ No se encontraron estadísticas para {nombre}.")
else:
    df_jugador = df_jugador.sort_values(by="Date")

    # Mostrar estadísticas por día
    for _, row in df_jugador.iterrows():
        fecha = row["Date"]
        ab = int(row["AB"])
        h = int(row["H"])
        double = int(row["2B"])
        triple = int(row["3B"])
        hr = int(row["HR"])
        r = int(row["R"])
        rbi = int(row["RBI"])
        bb = int(row["BB"])
        so = int(row["SO"])
        sb = int(row["SB"])
        hbp = int(row.get("HBP", 0))  # A veces HBP no está

        print(f"\n🧾 Estadísticas ofensivas de {nombre} ({fecha}):")
        print(f"AB: {ab}, H: {h}, 2B: {double}, 3B: {triple}, HR: {hr}, R: {r}, RBI: {rbi}, BB: {bb}, HBP: {hbp}, SO: {so}, SB: {sb}")
