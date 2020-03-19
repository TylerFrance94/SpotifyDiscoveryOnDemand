import spotipy
import datetime
import numpy as np
import spotipy.util as util
from random import seed
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'yourclientid' 
client_secret = 'yourclientsecret' 
username = 'yourusername' #input your username; can be found on accounts.spotify.com
url = 'urlofplaylist' #urlofplaylist
scope = 'playlist-modify-public, playlist-modify-private'

mydate = datetime.datetime.now()
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def createPlaylist(songlist):
    token = util.prompt_for_user_token(username,
                                       scope,
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri='http://localhost:8888/callback/')
    if not token:
        print("Can't get token for", username)
        raise Exception('Token error')

    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_create('513rxnyfbivo3ruo3f815mi8r', 'Discover on demand: '
                                       + str(mydate.year) + str(mydate.month) + str(mydate.day))

    playlistid = playlist['id']

    for i in range(len(songlist)):
        trackid = [songs[i]]
        sp.user_playlist_add_tracks(username, playlistid, trackid)
        #print(results)


def getOwner(uri):
    # "username = uri.split('?')[0]"
    playlist_id = uri.split('?')[0]
    results = sp.playlist(playlist_id)
    owner = results['owner']['id']
    return owner


def getArtists(uri):
    playlist_id = uri.split('?')[0]
    results = sp.playlist(playlist_id)
    i = 0
    artist = []
    for r in results['tracks']['items']:
        artist.append(results['tracks']['items'][i]['track']['artists'][0]['uri'])
        i += 1

    return artist


def relatedArtists(artists):
    relartist = []
    for i in range(len(artists) - 1):
        results = sp.artist_related_artists(artists[i])
        j = 0
        while j < len(results['artists']):
            relartist.append(results['artists'][j]['uri'])
            j += 1

    relartist = list(set(relartist))
    relartist = list(set(relartist) - set(artists))  # remove original artists if they got into the list
    return relartist


def randomArtists(relartists):
    randart = []
    for x in range(25):
        rand = np.random.randint(0, len(relartists) - 1)
        randart.append(relartists[rand])

    return randart


def getSongs(randomart):
    seed(1)
    randsongs = []
    for i in range(len(randomart)):
        artsongs = sp.artist_top_tracks(randomart[i])
        rand = np.random.randint(0, len(artsongs['tracks'])-1)
        randsongs.append(artsongs['tracks'][rand]['id'])

    return randsongs


owner = getOwner(url)
artists = getArtists(url)
relartists = relatedArtists(artists)
randomart = randomArtists(relartists)
songs = getSongs(randomart)
createPlaylist(songs)
