import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

APP_CLIENT_ID = YOUR_APP_CLIENT_ID
APP_CLIENT_SECRET = YOUR_APP_CLIENT_SECRET
REDIRECT_URI = "http://example.com"
Description = "Special Playlist"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=APP_CLIENT_ID,
                                               client_secret=APP_CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private"))
# username
user_id = sp.current_user()["id"]

input_date = input("Which year do you want to travel to? Type the date in the format YYYY-MM-DD ")

web_response = requests.get(f"https://www.billboard.com/charts/hot-100/{input_date}")
result = web_response.text

soup = BeautifulSoup(result, "html.parser")
titles_list = soup.find_all(name="h3", class_="u-letter-spacing-0021", id="title-of-a-story")
top_100_songs_names = [song.text.strip() for song in titles_list]


# to remove unwanted titles from the returned songs list
def remove_values(titles_list, unwanted_title):
    return [title for title in titles_list if title != unwanted_title]


renundant_items = ["Songwriter(s):", 'Producer(s):', 'Imprint/Promotion Label:']
for item in renundant_items:
    top_100_songs_names = remove_values(top_100_songs_names, item)

list_of_songs = []
year = input_date.split("-")[0]

# Searching Spotify for songs by title and the year you entered version
for song in top_100_songs_names:
    results = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        new_Result = results['tracks']['items'][0]['uri']
        # append the songs uri
        list_of_songs.append(new_Result)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create a user playlist with name as date billboard 100
playlist = sp.user_playlist_create(user=user_id, name=f"{input_date} BILLBOARD 100", public=False,
                                   description=Description)
sp.playlist_add_items(playlist_id=playlist["id"], items=list_of_songs)
