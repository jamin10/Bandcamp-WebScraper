# Bandcamp Webscraper v1.4

import requests
from bs4 import BeautifulSoup
import pandas as pd

# send request for webpage HTML
wisdomteeth_response = requests.get('https://wisdomteethuk.bandcamp.com/')
wisdomteeth = wisdomteeth_response.content

# convert HTML to BeautifulSoup object
wisdomteeth_soup = BeautifulSoup(wisdomteeth, "html.parser")

# Find all elements in an ol with class=title and add to a list
title_list = []
artist_list = []
music_grid = wisdomteeth_soup.find('ol', {'id', 'music-grid'})
for release in music_grid.find_all(attrs={'class':'title'}):
    # Split up elements into a list
    release_text = release.get_text('|').split('|')
    # Sometimes only has a track title so specify no artist
    # Add to title and artist lists
    if len(release_text) > 1:
        title_list.append(release_text[0])
        artist_list.append(release_text[1])
    else:
        title_list.append((release_text[0]))
        artist_list.append("none")

# Use strip to remove spaces and add to new list
strip_title_list = []
for el in title_list:
    strip_title_list.append(el.strip())
strip_artist_list = []
for ele in artist_list:
    strip_artist_list.append(ele.strip())

# Find links to release pages and add to list
links = []
music_grid_links = wisdomteeth_soup.find('ol', {'id', 'music-grid'})
for link in music_grid_links.find_all('a'):
    links.append(link.get('href'))

table = pd.DataFrame({
    "Artist":strip_artist_list, "Title":strip_title_list, "Link":links
})

table.to_excel(r'C:\Users\bpwhi\OneDrive\Documents\Work 2021\Python\WebScraper.xlsx', index=False)

print(table)


