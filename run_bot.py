import fetch_stats
import create_image

df = fetch_stats.get_performances()
print(df)

if df.empty:
    print("❌ No Dominican performances found.")
else:
    img = create_image.generate_table(df)
    print(f"✅ Image generated at: {img}")

