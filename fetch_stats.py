import requests
import pandas as pd
from datetime import datetime, timedelta

# Dominican players
DOMINICAN_PLAYERS = [
    "Rafael Devers", "Carlos Santana", "José Ramírez", "Willy Adames",
    "Víctor Robles", "Julio Rodríguez", "Jorge Polanco", "Miguel Andújar",
    "Christopher Morel", "Junior Caminero", "Leody Taveras", "Manny Machado",
    "Fernando Tatis Jr.", "Santiago Espinal", "Elly De La Cruz", "Jeimer Candelario",
    "Jeremy Peña", "Yainer Díaz", "Willi Castro", "Ramón Laureano", "Gary Sánchez",
    "Jorge Mateo", "Vladimir Guerrero Jr.", "Juan Soto", "Mark Vientos",
    "José Siri", "Starling Marte", "Jasson Domínguez", "Austin Wells",
    "Enmanuel Valdez", "Oneil Cruz", "Teoscar Hernández", "Geraldo Perdomo",
    "Luis Garcia Jr."
]

BASE_URL = "https://statsapi.mlb.com/api/v1"

def get_yesterdays_games():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"{BASE_URL}/schedule/games/?sportId=1&startDate={yesterday}&endDate={yesterday}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    game_ids = [game['gamePk'] for date in data['dates'] for game in date['games']]
    return game_ids

def get_boxscore(game_id):
    url = f"{BASE_URL}/game/{game_id}/boxscore"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def get_performances():
    games = get_yesterdays_games()
    players_data = []

    for game_id in games:
        box = get_boxscore(game_id)

        for team in ['home', 'away']:
            if team not in box or 'players' not in box[team]:
                continue

            players = box[team]['players']
            for player_id, player_info in players.items():
                stats = player_info.get('stats', {}).get('batting', {})
                if not stats:
                    continue

                name = player_info['person']['fullName']
                if name not in DOMINICAN_PLAYERS:
                    continue

                players_data.append({
                    "Player": name,
                    "AB": stats.get('atBats', 0),
                    "H": stats.get('hits', 0),
                    "2B": stats.get('doubles', 0),
                    "3B": stats.get('triples', 0),
                    "HR": stats.get('homeRuns', 0),
                    "R": stats.get('runs', 0),
                    "RBI": stats.get('rbi', 0),
                    "BB": stats.get('baseOnBalls', 0),
                    "SO": stats.get('strikeOuts', 0),
                    "SB": stats.get('stolenBases', 0)
                })

    return pd.DataFrame(players_data)
