import datetime
import math
import os  # Import the os module
import requests
import matplotlib.pyplot as plt
from io import BytesIO

USERNAME = 'Sayak_k'
TIME_CLASS = 'rapid'
RULES = 'chess'  
NGAMES = 50
headers = {"User-Agent": "ChessRatingRefresh/1.0 sayak.kr.dutta@gmail.com"}
ARCHIVES_URL = 'https://api.chess.com/pub/player/{user}/games/archives'

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

    # Create a buffer for the image data
    buffer = BytesIO()
    plt.savefig(buffer, format='png')  # Save the plot to the buffer as PNG
    buffer.seek(0)  # Reset the buffer position to the beginning
    
    # Set the directory where you want to save the file
    save_directory = "assets/"
    file_path = os.path.join(save_directory, 'plot.png')  # Construct the file path
    
    with open(file_path, "wb") as f:
        f.write(buffer.read())  # Write the image data from the buffer to the file
    
    buffer.close()  # Close the buffer
   
if __name__ == "__main__":
    main()
