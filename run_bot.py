import fetch_stats, create_image

df = fetch_stats.get_performances()
if df.empty:
    print("❌ No performances to show.")
else:
    create_image.generate_table(df)


