# classify.py

def clasificar_actuacion(h, hr, r, rbi, bb):
    if h >= 2:
        return "✅"
    if hr > 0 or r >= 2 or rbi >= 2 or (h == 1 and (r > 0 or rbi > 0)) or bb >= 2:
        return "✅"
    if h == 1 or bb > 0 or r > 0 or rbi > 0:
        return "⚠️"
    return "❌"
