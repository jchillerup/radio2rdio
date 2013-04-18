__author__ = 'jch'

import requests
import bs4

class OneLoveFM(object):
    url = "http://1love.fm/last.php"

    def get_cur_track(self):
        r = requests.get(self.url)
        soup = bs4.BeautifulSoup(r.text)

        cur_song = [div.text for div in soup.find_all("div", attrs={"id": "track-1"})]

        return cur_song