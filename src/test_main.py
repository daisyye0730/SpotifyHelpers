import unittest
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import main
import os

class TestSpotifyHelper(unittest.TestCase):
    def set_up():
        cid = "8f3b28899c924ad891f7d88921d9715f"
        secret = "050c3476911342ab95b63d03d44a2158"
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        return sp 
    
    # def test_ask_for_playlist_link(self):
    #     url = "https://open.spotify.com/playlist/6snlZhdBpJK0cxYURvqhFU?si=8e7eb1f3db5f438b"
    #     sp = TestSpotifyHelper.set_up()
    #     (track_uris, playlist_uri, playlist_link) = main.ask_for_playlist_link(url, sp)
    #     self.assertEqual(playlist_uri, '6snlZhdBpJK0cxYURvqhFU')
    #     self.assertEqual(playlist_link, url)
    #     self.assertTrue(len(track_uris)>1)

    # def test_process_track(self):
    #     sp = TestSpotifyHelper.set_up()
    #     playlist_uri = '6snlZhdBpJK0cxYURvqhFU'
        #d = main.process_track(sp, playlist_uri)
        #self.assertTrue(d[sp.playlist_items(playlist_uri)['items'][0]["track"]["name"]])

    # def test_match_beat(self):
    #     sp = TestSpotifyHelper.set_up()
    #     playlist_uri = '6snlZhdBpJK0cxYURvqhFU'
    #     d = main.process_track(sp, playlist_uri)
    #     self.assertTrue(len(main.match_beat(d, 173))>0)

    # def test_match_beat_artist_genres(self):
    #     sp = TestSpotifyHelper.set_up()
    #     playlist_uri = '6snlZhdBpJK0cxYURvqhFU'
    #     d = main.process_track(sp, playlist_uri)
    #     self.assertTrue(len(main.match_beat_artist_genres(d, 'pop'))>0)
        
    # def test_sort_by_beat(self): 
    #     sp = TestSpotifyHelper.set_up()
    #     playlist_uri = '6snlZhdBpJK0cxYURvqhFU'
    #     d = main.process_track(sp, playlist_uri)
    #     tempos = []
    #     for ele in main.sort_by_beat(d):
    #         tempos.append(ele[0])
    #     self.assertEqual(tempos, sorted(tempos))
        
    # def test_sort_by_pop(self):
    #     sp = TestSpotifyHelper.set_up()
    #     playlist_uri = '6snlZhdBpJK0cxYURvqhFU'
    #     d = main.process_track(sp, playlist_uri)
    #     popularity = []
    #     for ele in main.sort_by_pop(d):
    #         popularity.append(ele[0])
    #     self.assertEqual(popularity, sorted(popularity))
        
    def test_process_artist_album(self):
        if os.path.exists('../assets/img/nicole.jpg'): 
            os.remove('../assets/img/nicole.jpg')
        albumObj = main.process_artist_album('https://open.spotify.com/artist/2kxP07DLgs4xlWz8YHlvfh')
        self.assertTrue(len(albumObj)>0)
        self.assertTrue(os.path.exists('../assets/img/'+albumObj[0]["albumSlug"] + ".jpg"))

if __name__ == '__main__':
    unittest.main()