# filename: eiffel_tower_height.py

import requests
from bs4 import BeautifulSoup

# Send a GET request to the Wikipedia page of the Eiffel Tower
response = requests.get('https://en.wikipedia.org/wiki/Eiffel_Tower')

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the infobox on the page
infobox = soup.find('table', class_='infobox')

# Find the row that contains the height information
rows = infobox.find_all('tr')
for row in rows:
    if 'Height' in row.text:
        height_row = row
        break

# Extract the height value from the row
height = height_row.find('td').text.strip()

print("The height of the Eiffel Tower is:", height)