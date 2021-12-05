from configparser import ConfigParser
from spotipy.oauth2 import SpotifyOAuth
from artist import Artist
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
    user_id = sp.me()['id']
    genres_wanted = config.get('FILTER', 'genres_wanted').split(',')
    min_followers = config.getint('FILTER', 'min_followers')
    max_followers = config.getint('FILTER', 'max_followers')
    min_popularity = config.getint('FILTER', 'min_popularity')
    max_popularity = config.getint('FILTER', 'max_popularity')
    max_genre_count = config.getint('PLAYLIST', 'max_artists_per_genre')
    gems: list[Artist] = []
    for genre in genres_wanted:
        genre_count = 0
        print(f"{genre}:")
        limit = 50
        total = 1000
        for offset in range(0, total, limit):
            response = sp.search(f'genre:{genre}', type='artist', limit=limit, offset=offset)
            artists: list[Artist] = [Artist(_) for _ in response['artists']['items']]
            for artist in artists:
                if genre_count > max_genre_count:
                    break
                if (min_followers <= artist.followers <= max_followers and
                        min_popularity <= artist.popularity <= max_popularity):
                    genre_count += 1
                    print(artist)
                    if config.has_option('PLAYLIST_IDS', genre):
                        playlist_id = config.get('PLAYLIST_IDS', genre)
                    else:
                        playlist_id = sp.user_playlist_create(
                            user_id,
                            config.get('PLAYLIST', 'name').format(genre=genre),
                            public=config.getboolean('PLAYLIST', 'public')
                        )['id']

                        config.set('PLAYLIST_IDS', genre, playlist_id)
                        with open('config.ini', 'w') as f:
                            config.write(f)

                        print(f"Created playlist Gems: {genre}")

                    top_tracks = sp.artist_top_tracks(artist.id)['tracks']
                    sp.playlist_remove_all_occurrences_of_items(
                        playlist_id,
                        [track['id'] for track in top_tracks[:config.getint('PLAYLIST', 'tracks_per_artist')]]
                    )
                    sp.playlist_add_items(
                        playlist_id,
                        [track['id'] for track in top_tracks[:config.getint('PLAYLIST', 'tracks_per_artist')]]
                    )
