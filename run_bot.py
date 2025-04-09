import fetch_stats

# Obtener los datos ofensivos
df = fetch_stats.get_performances()

# Mostrar el resultado
print("🧾 Jugadores encontrados con stats ofensivos:")
print(df)

# Mensaje adicional si no hay data
if df.empty:
    print("❌ No se encontraron actuaciones ofensivas reales.")
else:
    print(f"✅ Total de jugadores listados: {len(df)}")


