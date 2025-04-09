from pybaseball import statcast_batter, playerid_lookup
import pandas as pd

# Buscar el ID de Juan Soto
soto_info = playerid_lookup("soto", "juan")
soto_id = soto_info.loc[0, "key_mlbam"]
print(f"📌 ID de Juan Soto: {soto_id}")

# Descargar data de Statcast para ese día
df = statcast_batter("2025-04-07", "2025-04-07", soto_id)

if df.empty:
    print("❌ Juan Soto no tuvo actividad ofensiva ese día.")
else:
    print(f"✅ {len(df)} lanzamientos registrados para Juan Soto.")

    # Filtrar solo eventos con valor (no NaN)
    eventos_realizados = df[df['events'].notna()][['player_name', 'events']]

    # Mostrar resultados
    pd.set_option("display.max_rows", None)
    print("\n🧾 Eventos ofensivos reales:")
    print(eventos_realizados)
