""" Unfollow playlists from config.ini """

from configparser import ConfigParser
from spotipy.oauth2 import SpotifyOAuth
import spotipy

if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')

    scopes = [
        'playlist-modify-private',
        'playlist-modify-public'
    ]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.get('SPOTIFY', 'client_id'),
        client_secret=config.get('SPOTIFY', 'client_secret'),
        redirect_uri=config.get('SPOTIFY', 'redirect_uri'),
        scope=scopes
    ))

    playlists = config.items('PLAYLIST_IDS')
    for genre, playlist_id in playlists:
        playlist_name = sp.playlist(playlist_id)['name']
        sp.current_user_unfollow_playlist(playlist_id)
        config.remove_option('PLAYLIST_IDS', genre)
        with open('config.ini', 'w') as f:
            config.write(f)
        print(f'Unfollowed playlist "{playlist_name}"')
