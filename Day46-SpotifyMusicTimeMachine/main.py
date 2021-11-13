from billboard_interface import BillboardInterface
from spotify_interface import SpotifyInterface


if __name__ == "__main__":
    billboard_interface = BillboardInterface()

    playlist_name = f"Top Hits from {billboard_interface.billboard_date}"
    spotify_interface = SpotifyInterface()
    spotify_interface.create_top_100_playlist(tracks=billboard_interface.tracks, playlist_name=playlist_name)

