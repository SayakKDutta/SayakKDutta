import datetime
import math
import requests
import matplotlib.pyplot as plt
import os
import base64

USERNAME = 'Sayak_k'
TIME_CLASS = 'rapid'
RULES = 'chess'  # chess960 and other variants possible here 1
NGAMES = 50
headers = {"User-Agent": "ChessRatingRefresh/1.0 sayak.kr.dutta@gmail.com"}
ARCHIVES_URL = 'https://api.chess.com/pub/player/{user}/games/archives'

# Define the path to save the plot locally
LOCAL_PLOT_PATH = 'plot.png'
# Define the path to save the plot in the repository
REPO_PLOT_PATH = 'plot.png'
# Define the GitHub repository details
REPO_OWNER = 'SayakKDutta'
REPO_NAME = 'SayakKDutta'
ACCESS_TOKEN = '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'

def get_archives() -> list:
    archives_dict = requests.get(url=ARCHIVES_URL.format(user=USERNAME), headers=headers).json()
    monthly_archives = archives_dict.get('archives')
    if monthly_archives is None:
        return []
    return monthly_archives[::-1]

def get_filtered_games(monthly_archive_url: str) -> list:
    games_dict = requests.get(url=monthly_archive_url, headers=headers).json()
    monthly_games = games_dict.get('games')
    if monthly_games is None:
        return []
    _filtered_games = list(filter(lambda game: game['time_class'] == TIME_CLASS, monthly_games))
    filtered_games = list(filter(lambda game: game['rules'] == RULES, _filtered_games))
    return filtered_games[::-1]

def get_ratings_from_games(games: list) -> list:
    ratings = []
    for game in games:
        if game['white']['username'] == USERNAME:
            ratings.append(game['white']['rating'])
        else:
            ratings.append(game['black']['rating'])
    return ratings[::-1]

def get_current_rating() -> int:
    pass

def main():
    final_games = []
    archives = get_archives()
    for archive in archives:
        games = get_filtered_games(archive)
        if games:
            final_games += games
        if len(final_games) >= NGAMES:
            break
    final_games = final_games[:NGAMES]
    ratings_list = get_ratings_from_games(final_games)
    
    plt.figure(figsize=(10, 6))
    plt.plot(ratings_list)
    plt.title('Chess Rating Over Time', color='blue')
    plt.xlabel('Number of Games', color='red')
    plt.ylabel('Chess.com Rating', color='red')
    plt.grid(False)
    plt.gca().set_facecolor('beige')  # Set background color
    plt.savefig(LOCAL_PLOT_PATH)  # Save the plot locally in Colab environment
    plt.show()

    # Upload the plot to GitHub repository
    upload_file_to_github(REPO_PLOT_PATH)

def upload_file_to_github(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode('utf-8')

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}'
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        'message': 'Add plot generated by script',
        'content': encoded_content
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 201:
        print('File uploaded successfully.')
    else:
        print(f'Error: {response.status_code}')

if __name__ == "__main__":
    main()