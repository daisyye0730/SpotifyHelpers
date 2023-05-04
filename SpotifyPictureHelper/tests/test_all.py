from SpotifyPictureHelper import main as spotify
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import os
import pytest
import cv2
import numpy as np


def check_file_exists_and_delete(path):
    f = open(path, "rb")
    yield f
    f.close()
    os.remove(path)


class TestSpotifyHelper:
    def test_make_request(self):
        response = spotify.make_request('https://open.spotify.com/user/rosycarina')
        assert response.url == 'https://open.spotify.com/user/rosycarina'

    @patch('requests.get')
    def test_get_soup(self, mock_requests):
        # mocking HTTP response
        mock_response = MagicMock()
        mock_response.content = "<!DOCTYPE html>\n"
        soup = spotify.get_soup(mock_response)
        # asserting that the soup text and mock response text are the same
        assert mock_response.content == soup.prettify()

    def test_process_user_profile_pic(self):
        # fake HTML to create BeautifulSoup object
        with open(os.path.join(os.sys.path[0], "fakeUser.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.process_user_profile_pic(soup) == (
                'rosycarina',
                'https://i.scdn.co/image/ab6775700000ee85c88b63d30ae5472bf4bee010',
            )

    def test_process_user_profile_pic_with_path(self):
        # fake HTML to create BeautifulSoup object
        with open(os.path.join(os.sys.path[0], "fakeUser.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.process_user_profile_pic(soup, img_path='./images/test_img_user.jpg') == (
                'rosycarina',
                'https://i.scdn.co/image/ab6775700000ee85c88b63d30ae5472bf4bee010',
            ) and check_file_exists_and_delete('./images/test_img_user.jpg')

    def test_get_public_playlists_albums(self):
        with open(os.path.join(os.sys.path[0], "fakeUser.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.get_public_playlists_albums(soup) == ('rosycarina', 10)

    def test_get_public_playlists_albums_with_path(self):
        with open(os.path.join(os.sys.path[0], "fakeUser.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.get_public_playlists_albums(soup, img_path='./images/test_img_playlist.jpg') == (
                'rosycarina',
                10,
            ) and check_file_exists_and_delete('./images/test_img_playlist.jpg')

    def test_get_individual_album_covers_from_mosaic(self):
        pre = "https://lite-images-i.scdn.co/image/"
        string = "ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6"
        assert spotify.get_individual_album_covers_from_mosaic(
            'https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6'
        ) == [pre + string[:40], pre + string[40:80], pre + string[80:120], pre + string[120:]]

    def test_get_individual_album_covers_from_mosaic_with_path(self):
        pre = "https://lite-images-i.scdn.co/image/"
        string = "ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6"
        assert spotify.get_individual_album_covers_from_mosaic(
            'https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6',
            './images/test_mosaic.jpg',
        ) == [
            pre + string[:40],
            pre + string[40:80],
            pre + string[80:120],
            pre + string[120:],
        ] and check_file_exists_and_delete(
            './images/test_mosaic.jpg'
        )

    def test_get_individual_album_covers_from_mosaic_invalid_html(self):
        html = "skjfslf;ls"
        with pytest.raises(Exception):
            spotify.get_individual_album_covers_from_mosaic(html)

    def test_get_individual_album_covers_from_mosaic_incomplete_html(self):
        html = "https://mosaic.scdn.co/"
        with pytest.raises(Exception):
            spotify.get_individual_album_covers_from_mosaic(html)

    def test_get_individual_album_covers_from_mosaic_invalid_length(self):
        html = "https://mosaic.scdn.co/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164"
        with pytest.raises(Exception):
            spotify.get_individual_album_covers_from_mosaic(html)

    def test_get_playlist_profile_pic(self):
        with open(os.path.join(os.sys.path[0], "fakePlaylist.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.get_playlist_profile_pic(soup) == (
                'Daily Mix 4',
                "https://dailymix-images.scdn.co/v2/img/ab6761610000e5eb2f8dfdfeb85c3fc2d11b2ae2/4/en/default",
            )

    def test_get_playlist_profile_pic_with_path(self):
        with open(os.path.join(os.sys.path[0], "fakePlaylist.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.get_playlist_profile_pic(soup, img_path='./images/test_img_profile.jpg') == (
                'Daily Mix 4',
                "https://dailymix-images.scdn.co/v2/img/ab6761610000e5eb2f8dfdfeb85c3fc2d11b2ae2/4/en/default",
            ) and check_file_exists_and_delete('./images/test_img_profile.jpg')

    def test_process_artist_album(self):
        fake_html = ''
        with open(os.path.join(os.sys.path[0], "fakeArtist.html"), "r") as f:
            fake_html = f.read()
        soup = BeautifulSoup(fake_html, "html.parser")
        assert spotify.process_artist_album(soup)[0] == {
            'albumName': 'Midnights (3am Edition)',
            'albumLink': '/album/3lS1y25WAhcqJDATJK70Mq',
            'albumImageUrl': 'https://i.scdn.co/image/ab67616d00001e02e0b60c608586d88252b8fbc0',
            'albumSlug': 'midnights-(3am-edition)',
        }

    def test_process_artist_album_with_path(self):
        fake_html = ''
        with open(os.path.join(os.sys.path[0], "fakeArtist.html"), "r") as f:
            fake_html = f.read()
        soup = BeautifulSoup(fake_html, "html.parser")
        assert spotify.process_artist_album(soup, img_path='./images/test_img_slug.jpg')[0] == {
            'albumName': 'Midnights (3am Edition)',
            'albumLink': '/album/3lS1y25WAhcqJDATJK70Mq',
            'albumImageUrl': 'https://i.scdn.co/image/ab67616d00001e02e0b60c608586d88252b8fbc0',
            'albumSlug': 'midnights-(3am-edition)',
        } and check_file_exists_and_delete('./images/test_img_slug.jpg')

    def test_filter_all_other_color(self):
        fake_path_to_img = "SpotifyPictureHelper/tests/blackWhite.png"
        fake_threshold_low = (0, 0, 0)
        fake_threshold_high = (30, 30, 30)
        new_img = spotify.filter_all_other_color(fake_path_to_img, fake_threshold_low, fake_threshold_high)
        count = len(new_img) * len(new_img[0])
        c = 0
        for i in range(0, len(new_img)):
            for j in range(0, len(new_img[0])):
                pix = new_img[i][j]
                if pix.all() == 255:
                    continue
                c += 1
        assert count == c

    def test_filter_all_other_color_with_no_valid_path(self):
        fake_path_to_img = "xxx/blackWhite.png"
        with pytest.raises(Exception):
            spotify.filter_all_other_color(fake_path_to_img, (0, 0, 0), (30, 30, 30))

    def test_filter_this_color(self):
        fake_path_to_img = "SpotifyPictureHelper/tests/blackWhite.png"
        fake_threshold_low = (200, 200, 200)
        fake_threshold_high = (255, 255, 255)
        new_img = spotify.filter_this_color(fake_path_to_img, fake_threshold_low, fake_threshold_high)
        count = len(new_img) * len(new_img[0])
        c = 0
        for i in range(0, len(new_img)):
            for j in range(0, len(new_img[0])):
                pix = new_img[i][j]
                if pix.all() == 255:
                    continue
                c += 1
        assert count == c

    def test_filter_this_color_with_no_valid_path(self):
        fake_path_to_img = "xxx/blackWhite.png"
        with pytest.raises(Exception):
            spotify.filter_this_color(fake_path_to_img, (0, 0, 0), (30, 30, 30))

    def test_smooth_img(self):
        fake_path_to_img = "SpotifyPictureHelper/tests/blackWhite.png"
        img = cv2.imread(fake_path_to_img)
        assert spotify.smooth_img(fake_path_to_img).all() == cv2.blur(img, (5, 5)).all()

    def test_smooth_img_with_no_valid_path(self):
        fake_path_to_img = "xxx/blackWhite.png"
        with pytest.raises(Exception):
            spotify.smooth_img(fake_path_to_img)

    def test_return_most_common_color(self):
        fake_path = "SpotifyPictureHelper/tests/test2.png"
        result = spotify.return_most_common_color(fake_path)
        assert result[0] == (255, 255, 255)

    def test_return_most_common_color_with_no_valid_path(self):
        fake_path_to_img = "xxx/blackWhite.png"
        with pytest.raises(Exception):
            spotify.return_most_common_color(fake_path_to_img)

    def test_overlay_two_images(self):
        fake_path_to_img1 = "SpotifyPictureHelper/tests/test2.png"
        img1 = cv2.imread(fake_path_to_img1)
        new_img = np.zeros(img1.shape[:2])
        cv2.imwrite("SpotifyPictureHelper/tests/overlay.png", new_img)
        img = spotify.overlay_two_images(fake_path_to_img1, "SpotifyPictureHelper/tests/overlay.png", 0.5, 0.5)
        count = 0
        for i in range(0, len(img)):
            for j in range(0, len(img[0])):
                pix = img[i][j]
                if pix.all() != 255:
                    count += 1
        assert count == img1.shape[0] * img1.shape[1]

    def test_overlay_two_images_with_two_different_sizes(self):
        fake_path_to_img1 = "SpotifyPictureHelper/tests/test2.png"
        fake_path_to_img2 = "SpotifyPictureHelper/tests/blackWhite.png"
        with pytest.raises(Exception):
            spotify.overlay_two_images(fake_path_to_img1, fake_path_to_img2, 1, 0)
