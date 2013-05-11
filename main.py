__author__ = 'jch'

import signal
from rdio import RdioClient
from generic import GenericPoller

rdio = RdioClient()
radio = GenericPoller(rdio.add_best_match, "http://radio.nulab.si:8800/onelove", "onelove.txt")

cmd = ""
while cmd != "exit":
    cmd = raw_input("> ")
    
    if cmd == "get":
        print radio.get_cur_track()
        
    if cmd == "add":
        rdio.add_song_to_playlist(rdio.get_best_match(radio.get_cur_track()))
