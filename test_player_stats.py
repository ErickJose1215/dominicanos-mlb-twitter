from pybaseball import statcast_batter, playerid_lookup
import pandas as pd

# Buscar ID de Juan Soto
soto_info = playerid_lookup("soto", "juan")
soto_id = soto_info.loc[0, "key_mlbam"]
print(f"📌 ID de Juan Soto: {soto_id}")

# Descargar datos del 1 al 8 de abril
df = statcast_batter("2025-04-01", "2025-04-08", soto_id)

if df.empty:
    print("❌ Juan Soto no tuvo actividad ofensiva en ese rango.")
else:
    # Asegurar columnas para evitar errores
    if 'rbi' not in df.columns:
        df['rbi'] = 0
    if 'scoring_play' not in df.columns:
        df['scoring_play'] = False

    # Filtrar eventos válidos
    eventos_df = df[df['events'].notna()][
        ['game_date', 'events', 'rbi', 'scoring_play']
    ]

    # Agrupar por fecha
    grouped = (
        eventos_df
        .groupby('game_date')
        .agg({
            'events': list,
            'rbi': 'sum',
            'scoring_play': lambda x: x.sum()
        })
        .reset_index()
        .sort_values(by='game_date')
    )

    # Procesar y mostrar
    for _, row in grouped.iterrows():
        fecha = row['game_date']
        eventos = row['events']
        rbi = int(row['rbi'])
        runs = int(row['scoring_play'])

        hits = ['single', 'double', 'triple', 'home_run']
        outs = ['field_out', 'force_out', 'grounded_into_double_play', 'other_out', 'strikeout']
        walks = ['walk', 'intent_walk']
        hbp = ['hit_by_pitch']
        steals = ['stolen_base']

        ab = sum(1 for e in eventos if e in hits + outs)
        h = sum(1 for e in eventos if e in hits)
        double = eventos.count('double')
        triple = eventos.count('triple')
        hr = eventos.count('home_run')
        bb = sum(1 for e in eventos if e in walks)
        hbp_count = eventos.count('hit_by_pitch')
        so = eventos.count('strikeout')
        sb = eventos.count('stolen_base')

        print(f"\n🧾 Estadísticas ofensivas de Juan Soto ({fecha}):")
        print(f"AB: {ab}, H: {h}, 2B: {double}, 3B: {triple}, HR: {hr}, R: {runs}, RBI: {rbi}, BB: {bb}, HBP: {hbp_count}, SO: {so}, SB: {sb}")
