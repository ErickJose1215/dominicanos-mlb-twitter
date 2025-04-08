from pybaseball import batting_stats_range
import pandas as pd
from datetime import datetime, timedelta

def get_performances():
    # Fecha principal: ayer
    main_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    fallback_date = "2024-09-15"  # Fecha conocida con actividad

    print(f"📅 Intentando obtener estadísticas ofensivas del {main_date}")

    try:
        df = batting_stats_range(main_date, main_date)
    except Exception as e:
        print(f"❌ Error consultando pybaseball para {main_date}: {e}")
        print(f"🔁 Reintentando con fecha segura: {fallback_date}")
        try:
            df = batting_stats_range(fallback_date, fallback_date)
        except Exception as e2:
            print(f"❌ Fallback también falló: {e2}")
            return pd.DataFrame()

    if df.empty:
        print("⚠️ No se encontraron estadísticas ofensivas.")
        return pd.DataFrame()

    # Seleccionar columnas clave
    columnas = ["Name", "AB", "H", "2B", "3B", "HR", "R", "RBI", "BB", "SO", "SB"]
    df_filtrado = df[columnas].copy()

    # Filtrar jugadores sin turnos al bate
    df_filtrado = df_filtrado[df_filtrado["AB"] > 0]

    if df_filtrado.empty:
        print("⚠️ Ningún jugador con AB > 0.")
    else:
        print(f"✅ {len(df_filtrado)} bateadores encontrados con stats útiles.")

    return df_filtrado.reset_index(drop=True)
