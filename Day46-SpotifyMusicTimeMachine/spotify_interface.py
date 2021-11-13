import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = ""          # @TODO
SPOTIPY_CLIENT_SECRET = ""      # @TODO
SPOTIPY_REDIRECT_URI="http://example.com/"

SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/"

scope = "playlist-modify-private"


class SpotifyInterface:

    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                      client_secret=SPOTIPY_CLIENT_SECRET,
                                      redirect_uri=SPOTIPY_REDIRECT_URI,
                                      scope=scope))
        self.current_user = self.sp.current_user()

        # for idx, item in enumerate(self.results["items"]):
        #     track = item["track"]
        #     print(idx, track["artists"][0]["name"], " - ", track["name"])

    def create_top_100_playlist(self, tracks: list[dict], playlist_name):
        """
            search for songs
            create playlist
            add songs to playlist
        """
        track_ids = self.search_for_tracks(tracks=tracks)
        playlist_id = self.create_playlist(name=playlist_name)
        self.add_top_100_songs(playlist_id=playlist_id, tracks=track_ids)

    def search_for_tracks(self, tracks: list[dict]) -> list:
        """
            returns a list of all track ids, for the track names passed in
        """
        track_ids = []
        for track in tracks:
            response = self.sp.search(q=f"track:{track['title']} artist:{track['artist']}", limit=1, type="track", market="US")
            try:
                track_ids.append(response["tracks"]["items"][0]["id"])
            except IndexError:
                print("A song could not be found or is unavailable. Skipping....")

        return track_ids

    def create_playlist(self, name) -> str:
        """
            returns id of created playlist
        """
        new_playlist = self.sp.user_playlist_create(user=self.current_user["id"], name=name, public=False)
        return new_playlist["id"]

    def add_top_100_songs(self, playlist_id, tracks):

        self.sp.playlist_add_items(playlist_id=playlist_id, items=tracks)

