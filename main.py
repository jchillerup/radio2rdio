__author__ = 'jch'

from onelove import OneLoveFM
from rdio import RdioClient

if __name__ == "__main__":
    radio = OneLoveFM()
    rdio = RdioClient()

    cmd = ""
    while cmd != "exit":
        cmd = raw_input("> ")

        if cmd == "get":
            print radio.get_cur_track()

        if cmd == "add":
            rdio.add_song_to_playlist(rdio.get_best_match(radio.get_cur_track()))
