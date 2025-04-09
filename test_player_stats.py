from pybaseball import batting_stats_range
import pandas as pd

# Player info and date range
player_name = "Juan Soto"
start_date = "2025-04-01"
end_date = "2025-04-08"

print(f"📅 Fetching stats for {player_name} from {start_date} to {end_date}...")

try:
    df = batting_stats_range(start_date, end_date)
except Exception as e:
    print(f"❌ Error fetching data: {e}")
    exit(1)

# Filter player by exact name
player_df = df[df['Name'] == player_name]

if player_df.empty:
    print(f"⚠️ No stats found for {player_name} in that range.")
else:
    player_df = player_df.sort_values(by="Date")

    for _, row in player_df.iterrows():
        date = row["Date"]
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
        hbp = int(row.get("HBP", 0))  # fallback if HBP column missing

        print(f"\n🧾 Offensive stats for {player_name} on {date}:")
        print(f"AB: {ab}, H: {h}, 2B: {double}, 3B: {triple}, HR: {hr}, R: {r}, RBI: {rbi}, BB: {bb}, HBP: {hbp}, SO: {so}, SB: {sb}")
