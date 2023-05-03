# SpotifyPictureHelper [![PyPI](https://img.shields.io/pypi/v/SpotifyPictureHelper)](https://pypi.org/project/SpotifyPictureHelper)[![docs](https://img.shields.io/badge/-docs-black?style=flat-square)](https://daisyye0730.github.io/SpotifyPictureHelper/docs/_build/html/index.html) 
This is a library of helper functions that allows users to process images in Spotify. 

![Hex.pm](https://img.shields.io/hexpm/l/apa?style=plastic)
![Hex.pm](https://img.shields.io/github/issues/daisyye0730/spotify_find_beats)
[![Package Status](https://img.shields.io/github/actions/workflow/status/daisyye0730/spotify_find_beats/build.yml)](https://github.com/daisyye0730/spotify_find_beats/)
[![codecov](https://codecov.io/gh/daisyye0730/SpotifyPictureHelper/branch/main/graph/badge.svg)](https://codecov.io/gh/daisyye0730/SpotifyPictureHelper)
[![PyPI](https://img.shields.io/pypi/v/SpotifyPictureHelper)](https://pypi.org/project/SpotifyPictureHelper/)

## Overview
Some tasks that it performs include:

1. process_user_profile_pic: extracts user profile picture given its html

2. get_public_playlists_albums: extracts all public playlist album covers from a user's html page 

3. get_individual_album_covers_from_mosaic: extracts four individual cover photos from a mosaic cover photo

4. get_playlist_profile_pic: extracts the profile picture from a playlist 

5. process_artist_album: extracts all the album covers of an artist 

6. make_request: accepts a html string and requests a session with the html with a response code 

7. get_soup: accepts the return object from make_request and parses into content acceptable in tasks 1-5

8. filter_all_other_color: gets rid of all the color (BGR) that is not within a certain range and save those that are 

9. filter_this_color: filters the color (BGR) within a specific range and save those that aren't 

10. smooth_img: smoothes and blurs the image. Without the parameter threshold, it will default to (5, 5)

11. return_most_common_color: returns the most common color (BGR) and its count in a picture 

12. overlay_two_images: overlays two images with the same size on top of each other. Can change the weight of each image. 

## How to Use  
1. Install the library by running: pip install SpotifyPictureHelper

2. Import the library in Python by including from SpotifyPictureHelper import main

## Details
The following are commands included in the Makefile:
- `make develop`: install the library's dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `black` and `flake8`
- `make format`: autoformat this library with `black`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information (passes with coverage >50%)
- `make clean`: cleans the repo

## Examples 
1. To start: Call get_soup(make_request('https://open.spotify.com/user/rosycarina')) to get the BeautifulSoup object from a html page 
2. process_user_profile_pic(get_soup(make_request('https://open.spotify.com/user/rosycarina'))) will return the user profile picture 
3. get_public_playlists_albums(get_soup(make_request('https://open.spotify.com/user/rosycarina'))) will return all the album covers of the user's public playlists 
4. get_individual_album_covers_from_mosaic('https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6') will return the four individual images from this mosaic image 
5. get_playlist_profile_pic(get_soup(make_request('https://open.spotify.com/playlist/6snlZhdBpJK0cxYURvqhFU?si=8e7eb1f3db5f438b&nd=1'))) will return the profile pic of this playlist
6. process_artist_album(get_soup(make_request('https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02'))) will return all the artist albums on the artist page.
7. filter_all_other_color("SpotifyPictureHelper/tests/test2.png", (0, 0, 0), (25, 25, 25)) leaves the image with pixels that fall between (0, 0, 0) and (25, 25, 25)
8. filter_this_color("SpotifyPictureHelper/tests/test2.png", (0, 0, 0), (25, 25, 25)) filters all pixels that fall between (0, 0, 0) and (25, 25, 25)
9. smooth_img("SpotifyPictureHelper/tests/test2.png") will smooth the image with the kernel size (5,5)
10. return_most_common_color("SpotifyPictureHelper/tests/test2.png") will return the most common color in this image file 
11. overlay_two_images("SpotifyPictureHelper/tests/test2.png", "SpotifyPictureHelper/tests/blackWhite.png", 0.5, 0.5) will return a blended image with the first image weighing 50% and the second image weighing also 50%
