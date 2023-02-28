import unittest
import main
import os


class TestSpotifyHelper(unittest.TestCase):
    def test_process_user_profile_pic(self):
        if os.path.exists("../assets/img/nbe3awe.jpg"):
            os.remove("../assets/img/nbe3awe.jpg")
        html = "https://open.spotify.com/user/11156981936"
        username = main.process_user_profile_pic(html)
        self.assertTrue(username)
        self.assertTrue(os.path.exists("../assets/img/" + username + ".jpg"))

    def test_process_user_profile_pic_invalid_html(self):
        html = "fjhsjfsf"
        with self.assertRaises(Exception):
            main.process_user_profile_pic(html)

    def test_process_user_profile_pic_incomplete_html(self):
        html = "https://open.spotify.com/user/"
        with self.assertRaises(Exception):
            main.process_user_profile_pic(html)

    def test_get_public_playlists_albums(self):
        if os.path.exists("../assets/img/nbe3awe_playlist_0.jpg"):
            os.remove("../assets/img/nbe3awe_playlist_0.jpg")
        html = "https://open.spotify.com/user/11156981936"
        username, num_albums = main.get_public_playlists_albums(html)
        self.assertTrue(num_albums > 0)
        self.assertTrue(username)
        self.assertTrue(
            os.path.exists("../assets/img/" + username + "_playlist_" + str(0) + ".jpg")
        )

    def test_get_public_playlists_albums_invalid_html(self):
        html = "fjklsjf;shfshiwepo"
        with self.assertRaises(Exception):
            main.get_public_playlists_albums(html)

    def test_get_public_playlists_albums_incomplete_html(self):
        html = "https://open.spotify.com/user/"
        with self.assertRaises(Exception):
            main.get_public_playlists_albums(html)

    def test_get_individual_album_covers_from_mosaic(self):
        for i in range(0, 4):
            if os.path.exists("../assets/img/mosaic_" + str(i) + ".jpg"):
                os.remove("../assets/img/mosaic_" + str(i) + ".jpg")
        link = "https://mosaic.scdn.co/60/ab67616d00001e0259a428dc7ef8e0c12b0fe18aab67616d00001e026892642704be8e8e60321c6aab67616d00001e027aede4855f6d0d738012e2e5ab67616d00001e02c5649add07ed3720be9d5526"
        imgs = main.get_individual_album_covers_from_mosaic(link)
        self.assertTrue(len(imgs) > 0)
        self.assertTrue(os.path.exists("../assets/img/mosaic_" + str(0) + ".jpg"))
        self.assertTrue(os.path.exists("../assets/img/mosaic_" + str(1) + ".jpg"))
        self.assertTrue(os.path.exists("../assets/img/mosaic_" + str(2) + ".jpg"))
        self.assertTrue(os.path.exists("../assets/img/mosaic_" + str(3) + ".jpg"))

    def test_get_individual_album_covers_from_mosaic_invalid_html(self):
        html = "skjfslf;ls"
        with self.assertRaises(Exception):
            main.get_individual_album_covers_from_mosaic(html)

    def test_get_individual_album_covers_from_mosaic_incomplete_html(self):
        html = "https://mosaic.scdn.co/"
        with self.assertRaises(Exception):
            main.get_individual_album_covers_from_mosaic(html)

    def test_get_individual_album_covers_from_mosaic_invalid_length(self):
        html = "https://mosaic.scdn.co/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164"
        with self.assertRaises(Exception):
            main.get_individual_album_covers_from_mosaic(html)

    def test_get_playlist_profile_pic(self):
        if os.path.exists("../assets/img/KPOP 2023 GIRL GROUPS TOP HITS_profile.jpg"):
            os.remove("../assets/img/KPOP 2023 GIRL GROUPS TOP HITS_profile.jpg")
        html = "https://open.spotify.com/playlist/5ija6EdKLl74z1YpwmwaIW"
        playlistName = main.get_playlist_profile_pic(html)
        self.assertTrue(len(playlistName) > 0)
        self.assertTrue(
            os.path.exists("../assets/img/" + playlistName + "_profile.jpg")
        )

    def test_get_playlist_profile_pic_invalid_html(self):
        html = "skjfslf;ls"
        with self.assertRaises(Exception):
            main.get_playlist_profile_pic(html)

    def test_get_playlist_profile_pic_incomplete_html(self):
        html = "https://open.spotify.com/playlist/"
        with self.assertRaises(Exception):
            main.get_playlist_profile_pic(html)

    def test_process_artist_album(self):
        if os.path.exists("../assets/img/nicole.jpg"):
            os.remove("../assets/img/nicole.jpg")
        albumObj = main.process_artist_album(
            "https://open.spotify.com/artist/2kxP07DLgs4xlWz8YHlvfh"
        )
        self.assertTrue(len(albumObj) > 0)
        self.assertTrue(
            os.path.exists("../assets/img/" + albumObj[0]["albumSlug"] + ".jpg")
        )

    def test_process_artist_album_invalid_html(self):
        html = "skjfslf;ls"
        with self.assertRaises(Exception):
            main.process_artist_album(html)

    def test_process_artist_album_incomplete_html(self):
        html = "https://open.spotify.com/artist/"
        with self.assertRaises(Exception):
            main.process_artist_album(html)


if __name__ == "__main__":
    unittest.main()
