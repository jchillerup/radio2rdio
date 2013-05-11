__author__ = 'jch'

import urllib2, threading, time

class GenericPoller(threading.Thread):
    def __init__(self, callback, url, log=None):
        threading.Thread.__init__(self)
        self.url = url
        self.callback = callback
        
        if log is not None:
            self.outfile = open(log, 'a+');

        self.daemon  = True
        self.start()


    def run(self):
        old_track = ""
        while True:
            cur_track = self.get_cur_track()

            if cur_track != old_track:
                if self.outfile is not None:
                    self.outfile.write("%s\n" % cur_track.encode('utf8'))
                    self.outfile.flush()

                self.callback(cur_track)
                old_track = cur_track

                time.sleep(60);

    def get_cur_track(self):
        request = urllib2.Request(self.url)

        request.add_header('Icy-MetaData', 1)
        response = urllib2.urlopen(request)
        icy_metaint_header = response.headers.get('icy-metaint')
        if icy_metaint_header is not None:
            metaint = int(icy_metaint_header)
            read_buffer = metaint+255
            content = response.read(read_buffer)
            title = content[metaint:].split("'")[1]
            return title

def callback(x):
    pass

if __name__ == '__main__':
    p = GenericPoller(callback, "http://radio.nulab.si:8800/onelove", "onelove.txt")
