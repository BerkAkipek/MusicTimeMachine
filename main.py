import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

DATE = input("Please enter a day in YYYY-MM-DD format in last 20 years.\n")
URL = f"https://www.billboard.com/charts/hot-100/{DATE}/"
CLIENT_SECRET = "YOUR CLIENT SECRET"
CLIENT_ID = "YOUR CLIENT ID"
REDIRECT_URI = "http://127.0.0.1:9090"

web_site = requests.get(URL)
soup = BeautifulSoup(web_site.text, "html.parser")

title_objects = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in title_objects]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = DATE.split("-")[0]
for song in song_names:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        print(f"Song: {song} does not exist in Spotify. Skipped")
        pass


playlist = sp.user_playlist_create(user=user_id, name=f"{DATE} BILLBOARD 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
