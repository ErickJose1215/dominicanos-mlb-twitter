from pybaseball import statcast_batter, playerid_lookup

# Buscar el MLB ID de Juan Soto
soto_info = playerid_lookup("soto", "juan")
soto_id = soto_info.loc[0, "key_mlbam"]

print(f"📌 ID de Juan Soto: {soto_id}")

# Obtener sus stats para el 7 de abril de 2025
df = statcast_batter("2025-04-07", "2025-04-07", soto_id)

if df.empty:
    print("❌ Juan Soto no tuvo actividad ofensiva ese día.")
else:
    print("✅ Stats de Juan Soto:")
    print(df[["player_name", "game_date", "description", "events"]])
