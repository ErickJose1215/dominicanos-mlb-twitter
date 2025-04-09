from pybaseball import statcast_batter, playerid_lookup
import pandas as pd
import time

# Lista de jugadores dominicanos (nombre, apellido)
dominican_players = [
    ("Juan", "Soto"),
    ("Julio", "Rodríguez"),
    ("Rafael", "Devers"),
    ("Fernando", "Tatis"),
    ("Teoscar", "Hernández")
]

start_date = "2025-04-07"
end_date = "2025-04-07"

for first, last in dominican_players:
    try:
        info = playerid_lookup(last, first)
        if info.empty:
            print(f"❌ Player not found: {first} {last}")
            continue

        player_id = info.loc[0, "key_mlbam"]
        full_name = f"{info.loc[0, 'name_first']} {info.loc[0, 'name_last']}"
        print(f"\n📌 Fetching data for {full_name} (ID: {player_id})")

        df = statcast_batter(start_date, end_date, player_id)
        if df.empty:
            print(f"⚠️ No offensive data for {full_name}.")
            continue

        if 'rbi' not in df.columns:
            df['rbi'] = 0
        if 'scoring_play' not in df.columns:
            df['scoring_play'] = False

        eventos_df = df[df['events'].notna()][
            ['game_date', 'events', 'rbi', 'scoring_play']
        ]

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

        if grouped.empty:
            print(f"⚠️ No offensive events found for {full_name}.")
            continue

        for _, row in grouped.iterrows():
            date = row['game_date']
            events = row['events']
            rbi = int(row['rbi'])
            runs = int(row['scoring_play'])

            hits = ['single', 'double', 'triple', 'home_run']
            outs = ['field_out', 'force_out', 'grounded_into_double_play', 'other_out', 'strikeout']
            walks = ['walk', 'intent_walk']
            hbp = ['hit_by_pitch']
            steals = ['stolen_base']

            ab = sum(1 for e in events if e in hits + outs)
            h = sum(1 for e in events if e in hits)
            double = events.count('double')
            triple = events.count('triple')
            hr = events.count('home_run')
            bb = sum(1 for e in events if e in walks)
            hbp_count = events.count('hit_by_pitch')
            so = events.count('strikeout')
            sb = events.count('stolen_base')

            print(f"\n🧾 Offensive stats for {full_name} on {date}:")
            print(f"AB: {ab}, H: {h}, 2B: {double}, 3B: {triple}, HR: {hr}, R: {runs}, RBI: {rbi}, BB: {bb}, HBP: {hbp_count}, SO: {so}, SB: {sb}")

        # Delay to avoid hammering the API
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error processing {first} {last}: {e}")
