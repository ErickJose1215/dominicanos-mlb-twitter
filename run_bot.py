import fetch_stats, create_image

df = fetch_stats.get_performances()
print(df)  # Ver contenido en los logs

if df.empty:
    print("❌ No performances found.")
else:
    img = create_image.generate_table(df)
    print(f"✅ Image generated at: {img}")
