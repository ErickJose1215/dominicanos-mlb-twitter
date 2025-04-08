# run_bot.py

import fetch_stats
import create_image

df = fetch_stats.get_performances()

if df.empty:
    print("❌ No Dominican performances found for yesterday.")
else:
    img = create_image.generate_table(df)
    print(f"✅ Image generated at: {img}")
