# -*- coding: utf-8 -*-
"""Rating_chess.com.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tvQLsqWlrUBcfC5ix6NlBHioN0xVmwF4
"""

import json
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import os


# Make a request to the API
username = "Sayak_K"
response = requests.get(f"https://www.chess.com/callback/user/popup/{username}")
data = response.json()

# Extract the required values
rating = int(data["bestRating"])
rating_type = data["bestRatingType"].upper()
puzzle_score = int(data["topPuzzleRushScore"])
puzzle_type = data["topPuzzleRushScoreType"].upper()

# Store the extracted values in capital letters and big size format
BEST_RATING = rating
BEST_RATING_TYPE = rating_type
TOP_PUZZLE_RUSH_SCORE = puzzle_score
TOP_PUZZLE_RUSH_SCORE_TYPE = puzzle_type


# Fetch the image content from GitHub
github_url = "https://github.com/SayakKDutta/SayakKDutta/blob/main/phpogr0qU.png?raw=true"
response = requests.get(github_url)
image_content = Image.open(BytesIO(response.content))

# Define the text to be printed in the PNG
# Define the text to be printed in the PNG
text = f"""
BEST RATING   {rating}

BEST RATING
   TYPE             {rating_type}

TOP PUZZLE
RUSH SCORE   {puzzle_score}

TOP PUZZLE
RUSH SCORE   {puzzle_type}
   TYPE
"""

# Create a figure with the same size as the background image
fig, ax = plt.subplots(figsize=(20, 8))

# Plot the background image
ax.imshow(image_content)

# Plot the text on top of the background image
ax.text(0, 0, text, va='top', ha='left', fontsize=24, color='white', fontweight='bold')

# Hide axes
ax.axis('off')

# Create a buffer for the image data
buffer = BytesIO()
plt.savefig(buffer, format='png')  # Save the plot to the buffer as PNG
buffer.seek(0)  # Reset the buffer position to the beginning

# Set the directory where you want to save the file
save_directory = "assets/"
os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist
file_path = os.path.join(save_directory, 'plot2.png')  # Construct the file path

# Write the image data from the buffer to the file
with open(file_path, "wb") as f:
    f.write(buffer.read())

buffer.close()  # Close the buffer

