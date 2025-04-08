from pybaseball import batting_stats_range
import pandas as pd
from datetime import datetime, timedelta

def get_performances():
    # Obtener la fecha de ayer en formato YYYY-MM-DD
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"📅 Obteniendo estadísticas ofensivas del {yesterday}")

    # Consultar todas las actuaciones de bateadores en ese día
    try:
        df = batting_stats_range(yesterday, yesterday)
    except Exception as e:
        print(f"❌ Error consultando pybaseball: {e}")
        return pd.DataFrame()

    # Seleccionar columnas clave
    columnas = ["Name", "AB", "H", "2B", "3B", "HR", "R", "RBI", "BB", "SO", "SB"]
    df_filtrado = df[columnas].copy()

    # Eliminar jugadores sin turnos al bate
    df_filtrado = df_filtrado[df_filtrado["AB"] > 0]

    if df_filtrado.empty:
        print("⚠️ No se encontraron actuaciones ofensivas con AB > 0.")
    else:
        print(f"✅ {len(df_filtrado)} bateadores con estadísticas encontradas.")

    return df_filtrado.reset_index(drop=True)
