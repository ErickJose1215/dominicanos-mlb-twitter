# create_image.py

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def generate_table(df):
    date_str = datetime.now().strftime("%d/%m/%Y")
    title1 = "DOMINICAN BATTERS IN MLB 🇩🇴"
    title2 = f"Performance for {date_str}"
    title3 = "Created by Erick Lantigua (@EJLantigua)"

    fig, ax = plt.subplots(figsize=(13, 1 + 0.4 * len(df)))
    ax.axis('off')

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#1f2a44')
        else:
            cell.set_facecolor('white')

    plt.figtext(0.5, 0.97, title1, ha='center', fontsize=16, weight='bold')
    plt.figtext(0.5, 0.94, title2, ha='center', fontsize=13)
    plt.figtext(0.5, 0.91, title3, ha='center', fontsize=10, style='italic')

    output_path = "dominican_batters.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path
