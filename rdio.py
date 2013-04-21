__author__ = 'jch'

import oauth2 as oauth
import urllib, json, urlparse, pickle
from credentials import API_KEY, API_SS
from fuzzywuzzy import fuzz

class RdioClient(object):
    endpoint = "http://api.rdio.com/1/"
    client = None
    playlist = "p2895869"

    def __init__(self):
        # Set up the OAuth business
        self.consumer = oauth.Consumer(API_KEY, API_SS)
        self.client = oauth.Client(self.consumer)

        try:
            access_content = pickle.load(file("token", "rb"))
        except IOError:
            access_content = None

        if access_content is not None:
            access_token = oauth.Token(access_content['oauth_token'], access_content['oauth_token_secret'])
            self.client = oauth.Client(self.consumer, access_token)
        else:
            self.authenticate()
        

    def authenticate(self):
        # http://developer.rdio.com/docs/rest/oauth
        response, content = self.client.request("http://api.rdio.com/oauth/request_token", "POST", urllib.urlencode({"oauth_callback": "oob"}));
        parsed_content = dict(urlparse.parse_qsl(content))
        request_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])

        print 'Authorize this application at: %s?oauth_token=%s' % (parsed_content['login_url'], parsed_content['oauth_token'])
        oauth_verifier = raw_input('Enter the PIN / OAuth verifier: ').strip()
        # associate the verifier with the request token
        request_token.set_verifier(oauth_verifier)
        
        # upgrade the request token to an access token
        tmp_client = oauth.Client(self.consumer, request_token)
        response, content = tmp_client.request('http://api.rdio.com/oauth/access_token', 'POST')
        parsed_content = dict(urlparse.parse_qsl(content))

        pickle.dump(parsed_content, file("token", "wb"))
        
        access_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])

        self.client = oauth.Client(self.consumer, access_token)
        
        
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

        print " + Searching for %s" % term[0]
        artist, track = term[0].lower().split(" - ");

        for result in response["result"]["results"]:
            r_artist, r_track = result["artist"].lower(), result["name"].lower()
            artist_score, track_score = fuzz.partial_ratio(artist, r_artist), fuzz.partial_ratio(track, r_track)

            print "%s - %s (%d/%d)" % (r_artist, r_track, artist_score, track_score)
            
            if  artist_score > 75 and track_score > 75:
                print " + Song added:     %s" % term[0]
                return result["key"]

        print " + Song not found: %s" % term[0]
        
        return None
        
    def add_song_to_playlist(self, song):
        if song is not None:
            response = self.call("addToPlaylist", {"playlist": self.playlist, "tracks": song})
        
