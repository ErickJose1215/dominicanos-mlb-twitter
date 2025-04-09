# fetch_stats.py

from pybaseball import statcast_batter, playerid_lookup
import pandas as pd
from datetime import datetime, timedelta
import time

# Lista de jugadores dominicanos (nombre completo)
DOMINICAN_PLAYERS = [
    "Juan Soto", "Rafael Devers", "Julio Rodríguez", "Fernando Tatis", "Teoscar Hernández"
]

START_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
END_DATE = START_DATE  # Solo el día anterior

def get_performances():
    rows = []

    for full_name in DOMINICAN_PLAYERS:
        try:
            first, last = full_name.split(" ", 1)
            info = playerid_lookup(last, first)

            if info.empty:
                print(f"❌ Player not found: {full_name}")
                continue

            player_id = info.loc[0, "key_mlbam"]
            df = statcast_batter(START_DATE, END_DATE, player_id)

            if df.empty:
                continue

            if 'rbi' not in df.columns:
                df['rbi'] = 0
            if 'scoring_play' not in df.columns:
                df['scoring_play'] = False

            events_df = df[df['events'].notna()][
                ['game_date', 'events', 'rbi', 'scoring_play']
            ]

            grouped = (
                events_df
                .groupby('game_date')
                .agg({
                    'events': list,
                    'rbi': 'sum',
                    'scoring_play': lambda x: x.sum()
                })
                .reset_index()
                .sort_values(by='game_date')
            )

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

                rows.append({
                    "Player": full_name,
                    "Date": date,
                    "AB": ab,
                    "H": h,
                    "2B": double,
                    "3B": triple,
                    "HR": hr,
                    "R": runs,
                    "RBI": rbi,
                    "BB": bb,
                    "HBP": hbp_count,
                    "SO": so,
                    "SB": sb
                })

            time.sleep(1)

        except Exception as e:
            print(f"❌ Error processing {full_name}: {e}")
            continue

    df_final = pd.DataFrame(rows)

    if df_final.empty:
        print("❌ No offensive stats found for any player.")
    else:
        df_final = df_final.sort_values(by=["H", "HR", "RBI"], ascending=False).reset_index(drop=True)

    return df_final
