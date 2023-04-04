import requests
from bs4 import BeautifulSoup


def make_request(html):
    """Makes a request given an html

    Args:
        html (string): html string 

    Returns:
        requests.Response object 

    """
    return requests.get(html)


def get_soup(request):
    """Takes a html request to be parsed 

    Args:
        request (requests.Response object): takes the return value of make_request

    Returns:
        Beautiful Soup Object 

    """
    return BeautifulSoup(request.content, "html.parser")


def process_user_profile_pic(soup: BeautifulSoup):
    """Finds the user profile picture given its soup
    
    Finds and saves the user profile picture locally.

    Args:
        soup (Beautiful Soup object): the beautiful soup object to be analyzed 

    Returns:
        tuple: returns the username of the profile and the link to access the image 

    """
    # find the img tag with the user's profile picture
    res = soup.findAll("img", {"data-testid": "user-entity-image"})
    src = res[0].get("src")
    # this is the profile image
    pic = make_request(f"{src}")
    # this is the user name
    head = soup.find("head")
    title = head.find("title")
    username = title.text.split(" ")[0]
    if pic.status_code == 200:
        with open(f"../{username}.jpg", "wb") as f:
            f.write(pic.content)
    else:
        raise Exception("Failed to fetch picture")
    return (username, src)


def get_public_playlists_albums(soup: BeautifulSoup):
    """Fetches and saves the public playlist album pictures 

    Given a user's profile's soup, fetches and saves all the album pictures of the public playlists the user has.

    Args:
        soup (BeautifulSoup object): return value of get_soup

    Returns:
        tuple: returns username and the number of public playlists found

    """
    res = soup.findAll("img")[1:]
    head = soup.find("head")
    title = head.find("title")
    username = title.text.split(" ")[0]
    src = res[0].get("src")
    for i in range(0, len(res)):
        ele = res[i]
        src = ele.get("src")
        pic = make_request(f"{src}")
        if pic.status_code == 200:
            with open(f"../{username}_playlist_{i}.jpg", "wb") as f:
                f.write(pic.content)
    return (username, len(res))


def get_individual_album_covers_from_mosaic(link):
    """Take one mosaic album cover and save four individual covers from it

    This is the function to get individual pictures from a mosaic album cover

    Args:
        link (string): The link of the mosaic album picture 

    Returns:
        list: a list of individual album picture links

    """
    # For example: "https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6"
    if "https://mosaic.scdn.co/" not in link:
        raise Exception("Invalid mosaic link, please make sure the link starts with https://mosaic.scdn.co/300/")
    split_link = link.split("/")
    if len(split_link) != 5:
        raise Exception("Depracated mosaic link, please try a new link")
    imgs = split_link[-1]
    li_imgs = []
    if len(imgs) != 160:
        return Exception("Sorry this link cannot be broken down")
    pre = "https://lite-images-i.scdn.co/image/"
    for i in range(0, 4):
        li_imgs.append(pre + imgs[i * 40 : (i + 1) * 40])
        pic = make_request(pre + imgs[i * 40 : (i + 1) * 40])
        if pic.status_code == 200:
            with open(f"../mosaic_{i}.jpg", "wb") as f:
                f.write(pic.content)
    return li_imgs


def get_playlist_profile_pic(soup):
    """Fetches and saves the cover picture of a playlist

    Args:
        soup (BeautifulSoup object): return value of get_soup 

    Returns:
        tuple: the name of the playlist and the link of the image 

    """
    res = soup.findAll("img")[0]
    # find playlist name
    name = soup.find("h1")
    playlist_name = name.text
    pic = make_request(res.get("src"))
    if pic.status_code == 200:
        with open(f"../{playlist_name}_profile.jpg", "wb") as f:
            f.write(pic.content)
    return (playlist_name, res.get("src"))


def process_artist_album(soup: BeautifulSoup):
    """Gets and saves the album covers given an artist

    Given the soup of the artist page, fetches all the album covers on that page and saves them locally.

    Args:
        soup (BeautifulSoup object): Return value of get_soup 

    Returns:
        list: a list of dictionaries, each dictionary contains the albumName, albumLink, albumImageUrl, and albumSlug 

    """
    # Find the h2 tag with text of Albums
    albumHeading = soup.find("h2", string="Albums")

    # Get the parent section
    albumSection = albumHeading.find_parent("div").find_parent("div")

    # Find all albums in the album section
    albums = albumSection.findAll("div")[1:]

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
        pic = make_request(f"{albumImage}")
        if pic.status_code == 200:
            with open(f"../{albumSlug}.jpg", "wb") as f:
                f.write(pic.content)
    return albumObj
