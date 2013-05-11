__author__ = 'jch'

import requests, bs4, threading, time

class OneLoveFM(threading.Thread):
    url = "http://1love.fm/last.php"
    outfile = None
    callback = None
    
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.outfile = open('onelove.txt', 'a+')
        self.daemon = True
        self.start()

    def run(self):
        print "Starting main thread"
        old_track = ""
        while True:
            cur_track = self.get_cur_track()

            if cur_track != old_track:
                self.outfile.write("%s\n" % cur_track.encode('utf8'))
                self.outfile.flush()
                
                self.callback(cur_track)
                old_track = cur_track
            
            time.sleep(60);
        
    def get_cur_track(self):
        r = requests.get(self.url)
        soup = bs4.BeautifulSoup(r.text)

        cur_song = [div.text for div in soup.find_all("div", attrs={"id": "track-1"})]

        return cur_song[0]
