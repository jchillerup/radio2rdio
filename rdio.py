__author__ = 'jch'

import oauth2 as oauth
import urllib
import json
from credentials import API_KEY, API_SS

class RdioClient(object):
    endpoint = "http://api.rdio.com/1/"
    client = None
    playlist = "p2895869"

    def __init__(self):
        # Set up the OAuth business
        consumer = oauth.Consumer(API_KEY, API_SS)
        self.client = oauth.Client(consumer)

    def authenticate():
        # http://developer.rdio.com/docs/rest/oauth
        response = self.call("request_token", {"request_token": "oob"});
        
    def call(self, method, data=dict()):
        payload = data
        payload["method"] = method

        response, content = self.client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode(payload))
        try:
            return json.loads(content)
        except ValueError:
            print response

    def register_playlist(self, key):
        self.playlist = key

    def list_playlists_by_user(self, user):
        response = self.call("findUser", {"vanityName": user})
        user_key = response['result']['key']

        response = self.call("getPlaylists", {"user": user_key})
        for playlist in response['result']['owned']:
            print playlist["key"] + ": " + playlist["name"]

    def get_best_match(self, term):
        response = self.call("search", {"query": term, "types": "Track"})

        # TODO: make sure it picks the best match

        return response["result"]["results"][0]["key"]

    def add_song_to_playlist(self, song):
        response = self.call("addToPlaylist", {"playlist": self.playlist, "tracks": song})
        print response
