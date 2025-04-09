from pybaseball import statcast_batter, playerid_lookup
import pandas as pd

# Buscar ID de Juan Soto
soto_info = playerid_lookup("soto", "juan")
soto_id = soto_info.loc[0, "key_mlbam"]
print(f"📌 ID de Juan Soto: {soto_id}")

# Descargar data
df = statcast_batter("2025-04-07", "2025-04-07", soto_id)

if df.empty:
    print("❌ Juan Soto no tuvo actividad ofensiva ese día.")
else:
    print(f"✅ {len(df)} lanzamientos registrados para Juan Soto.")

    # Filtrar eventos no nulos
    eventos = df[df['events'].notna()]['events'].tolist()

    # Definir tipos de eventos
    hits = ['single', 'double', 'triple', 'home_run']
    outs = ['field_out', 'force_out', 'grounded_into_double_play', 'other_out', 'strikeout']
    walks = ['walk', 'intent_walk']
    steals = ['stolen_base']
    hitbypitch = ['hit_by_pitch']

    # Calcular stats
    ab = sum(1 for e in eventos if e in hits + outs)
    h = sum(1 for e in eventos if e in hits)
    double = eventos.count('double')
    triple = eventos.count('triple')
    hr = eventos.count('home_run')
    bb = sum(1 for e in eventos if e in walks)
    so = eventos.count('strikeout')
    sb = eventos.count('stolen_base')
    hbp = eventos.count('hitbypitch')

    # Mostrar stats
    print(f"\n🧾 Estadísticas ofensivas de Juan Soto (2025-04-07):")
    print(f"AB: {ab}, H: {h}, 2B: {double}, 3B: {triple}, HR: {hr}, BB: {bb}, SO: {so}, SB: {sb}, HBP: {hbp}")
