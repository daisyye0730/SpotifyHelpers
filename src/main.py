import requests
from bs4 import BeautifulSoup

"""This is the function that gets the cover picture of a user"""
"""Input is a user playlist main page"""


def process_user_profile_pic(html):
    if "https://open.spotify.com/user/" not in html:
        raise Exception(
            "Invalid HTML, please make sure the link starts with https://open.spotify.com/user/"
        )
    page = requests.get(html)
    if page.status_code != 200:
        raise Exception("Invalid server response " + page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")
    # find the img tag with the user's profile picture
    res = soup.findAll("img", {"data-testid": "user-entity-image"})
    src = res[0].get("src")
    # this is the profile image
    pic = requests.get(f"{src}")
    # this is the user name
    head = soup.find("head")
    title = head.find("title")
    username = title.text.split(" ")[0]
    if pic.status_code == 200:
        with open(f"../assets/img/{username}.jpg", "wb") as f:
            f.write(pic.content)
    else:
        raise Exception("Failed to fetch picture")
    return username


"""This is the function that gets all the public playlist album cover pictures of a user"""
"""Input is a user playlist main page"""


def get_public_playlists_albums(html):
    if "https://open.spotify.com/user/" not in html:
        raise Exception(
            "Invalid HTML, please make sure the link starts with https://open.spotify.com/user/"
        )
    page = requests.get(html)
    if page.status_code != 200:
        raise Exception("Invalid server response " + page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")
    # find the img tag with the user's profile picture
    res = soup.findAll("img")[1:]
    # this is the user name
    head = soup.find("head")
    title = head.find("title")
    username = title.text.split(" ")[0]
    src = res[0].get("src")
    for i in range(0, len(res)):
        ele = res[i]
        src = ele.get("src")
        pic = requests.get(f"{src}")
        if pic.status_code == 200:
            with open(f"../assets/img/{username}_playlist_{i}.jpg", "wb") as f:
                f.write(pic.content)
    return (username, len(res))


"""This is the function to get individual pictures from a mosaic album cover"""
"""Input is a link of the mosaic image"""


def get_individual_album_covers_from_mosaic(link):
    # For example: "https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6"
    if "https://mosaic.scdn.co/" not in link:
        raise Exception(
            "Invalid mosaic link, please make sure the link starts with https://mosaic.scdn.co/300/"
        )
    split_link = link.split("/")
    if len(split_link) != 5:
        raise Exception("Depracated mosaic link, please try a new link")
    imgs = split_link[-1]
    if len(imgs) != 160:
        return Exception("Sorry this link cannot be broken down")
    pre = "https://lite-images-i.scdn.co/image/"
    for i in range(0, 4):
        pic = requests.get(pre + imgs[i * 40 : (i + 1) * 40])
        if pic.status_code == 200:
            with open(f"../assets/img/mosaic_{i}.jpg", "wb") as f:
                f.write(pic.content)
    return imgs


"""This is the function that gets the cover picture of a playlist"""
"""input is a playlist html"""


def get_playlist_profile_pic(html):
    if "https://open.spotify.com/playlist/" not in html:
        raise Exception(
            "Invalid mosaic link, please make sure the link starts with https://open.spotify.com/playlist/"
        )
    page = requests.get(html)
    if page.status_code != 200:
        raise Exception("Invalid server response " + page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")
    res = soup.findAll("img")[0]
    # find playlist name
    name = soup.find("h1")
    playlist_name = name.text
    pic = requests.get(res.get("src"))
    if pic.status_code == 200:
        with open(f"../assets/img/{playlist_name}_profile.jpg", "wb") as f:
            f.write(pic.content)
    return playlist_name


"""This is the function that gets the album covers on spotify given an artist"""
"""Input is first page of an artist"""


def process_artist_album(html):
    if "https://open.spotify.com/artist/" not in html:
        raise Exception(
            "Invalid mosaic link, please make sure the link starts with https://open.spotify.com/artist/"
        )
    # Open the Spotify source code file
    page = requests.get(html)
    if page.status_code != 200:
        raise Exception("Invalid server response " + page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the h2 tag with text of Albums
    albumHeading = soup.find("h2", string="Albums")
    # print(albumHeading)

    # Get the parent section
    albumSection = albumHeading.find_parent("div").find_parent("div")
    # print(albumSection)

    # Find all albums in the album section
    albums = albumSection.findAll("div")[1:]
    # print(albums)

    # Iterate through each album and get the data needed
    albumObj = []
    for album in albums:
        atag = album.find("a")
        if atag is None:
            continue
        href = f"{atag['href']}"
        albumName = atag.find("span").text
        albumSlug = albumName.replace(" ", "-").lower()
        albumImage = atag.find("img").get("src")
        albumDetails = {
            "albumName": albumName,
            "albumLink": href,
            "albumImageUrl": albumImage,
            "albumSlug": albumSlug,
        }

        albumObj.append(albumDetails)

        # Download the image at the image URL and save it in an images folder
        pic = requests.get(f"{albumImage}")
        if pic.status_code == 200:
            with open(f"../assets/img/{albumSlug}.jpg", "wb") as f:
                f.write(pic.content)
    return albumObj


# process_user_profile_pic('https://open.spotify.com/user/rosycarina')
# get_public_playlists_albums('https://open.spotify.com/user/rosycarina')
# process_artist_album("https://open.spotify.com/artist/2kxP07DLgs4xlWz8YHlvfh")
# get_individual_album_covers_from_mosaic("https://mosaic.scdn.co/640/ab67616d00001e021869a85947a5ea00df8c936fab67616d00001e023bb056e3160b85ee86c1194dab67616d00001e026887b017d077dfc5787a3e23ab67616d00001e02d70036292d54f29e8b68ec01")
# get_playlist_profile_pic("https://open.spotify.com/playlist/2VdX9qYAJXVfmFtefv0SmA")
