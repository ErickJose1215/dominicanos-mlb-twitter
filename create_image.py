import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def generate_table(df):
    fecha = datetime.now().strftime("%d/%m/%Y")
    titulo1 = "BATEADORES DOMINICANOS EN MLB 🇩🇴"
    titulo2 = f"Actuación del {fecha}"
    titulo3 = "Creado por Erick Lantigua (@EJLantigua)"

    fig, ax = plt.subplots(figsize=(13, 1 + 0.4 * len(df)))
    ax.axis('off')

    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center')

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1, 1.5)

    for (row, col), cell in tabla.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#1f2a44')
        else:
            cell.set_facecolor('white')

    plt.figtext(0.5, 0.97, titulo1, ha='center', fontsize=16, weight='bold')
    plt.figtext(0.5, 0.94, titulo2, ha='center', fontsize=13)
    plt.figtext(0.5, 0.91, titulo3, ha='center', fontsize=10, style='italic')

    output_path = "dominican_batters.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path
