__author__ = 'jch'

from onelove import OneLoveFM
from rdio import RdioClient

if __name__ == "__main__":
    radio = OneLoveFM()
    rdio = RdioClient()

    rdio.add_song_to_playlist(rdio.get_best_match(radio.get_cur_track()))

