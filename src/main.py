import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json 
import requests
from bs4 import BeautifulSoup

#Authentication - without user
def authenticate():
    credentials = json.load(open('authorization.json'))
    cid = credentials['client_id']
    secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

def ask_for_playlist_link(playlist_link, sp):
    # for example, playlist_link can be https://open.spotify.com/playlist/6snlZhdBpJK0cxYURvqhFU?si=8e7eb1f3db5f438b
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]  
    return (track_uris, playlist_URI, playlist_link)

def process_track(sp, playlist_URI):
    beats = {}
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        #URI
        track_uri = track["track"]["uri"]
    
        #Track name
        track_name = track["track"]["name"]
        
        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        
        #Name, popularity, genre
        artist_name = track["track"]["artists"][0]["name"]
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]
        
        #Album
        album = track["track"]["album"]["name"]
        
        #Popularity of the track
        track_pop = track["track"]["popularity"]
        
        audio = sp.audio_features(track_uri)[0]
        beats[track_name] = [track_uri, artist_uri, artist_info, artist_name, artist_pop, artist_genres, album, track_pop, audio['tempo']]
    return beats

# match beats without another constraint 
def match_beat(beats, target):
    result = []
    for b, descript in beats.items():
        if descript[-1] == target: 
            result.append(b)      
    return result

# match beats given a certain artist genre 
def match_beat_artist_genres(beats, genre):
    result = []
    for b, descript in beats.items():
        if descript[5] == genre: 
            result.append(b)      
    return result

# sort the songs by beats 
def sort_by_beat(beats):
    res = []
    for b, descript in beats.items():
        res.append((descript[-1], descript[4], b, descript[0]))
    res.sort()
    return res 
    
# sort the songs by popularity 
def sort_by_pop(beats):
    res = []
    for b, descript in beats.items():
        res.append((descript[4], descript[-1], b, descript[0]))
    res.sort()
    return res 

def process_artist_album(html):
    # Open the Spotify source code file
    page = requests.get(html)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the h2 tag with text of Albums
    albumHeading = soup.find("h2", string="Albums")
    #print(albumHeading)

    # Get the parent section
    albumSection = albumHeading.find_parent("div").find_parent("div")
    #print(albumSection)

    # Find all albums in the album section
    albums = albumSection.findAll("div")[1:]
    #print(albums)

    # Iterate through each album and get the data needed
    albumObj = []
    for album in albums:
        atag = album.find("a")
        if atag is None: 
            continue 
        href = f"{atag['href']}"
        albumName = atag.find("span").text
        albumSlug = albumName.replace(" ","-").lower()
        albumImage = atag.find("img").get('src')
        albumDetails = {
            "albumName": albumName,
            "albumLink": href,
            "albumImageUrl": albumImage
        }

        albumObj.append(albumDetails)
        print(albumName, albumImage, href)

        # Download the image at the image URL and save it in an images folder
        pic = requests.get(f"{albumImage}")
        if pic.status_code == 200:
            with open(f"../assets/img/{albumSlug}.jpg", 'wb') as f:
                f.write(pic.content)

# to test the function that scrapes the images 
#process_artist_album("https://open.spotify.com/artist/7tYKF4w9nC0nq9CsPZTHyP")